#!/Users/igoreremin/.envs/text_renderer/bin/python

import math
import os
import zipfile
from pathlib import Path
from typing import List

import click
import cv2 as cv

from render_config import RENDER_MASK

SHARD_SIZE = 1000


def get_image_files(images_dir: Path) -> List[Path]:
    image_files = []
    for img_file in sorted(images_dir.glob("*.jpg")):
        image_files.append(img_file)
    return image_files


def create_archive(dataset_dir: Path, archive_path: Path):
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(dataset_dir):
            for file in files:
                file_path = Path(root) / file
                arc_name = file_path.relative_to(dataset_dir)
                zf.write(file_path, arc_name)


def split_on_image_and_mask(
    image_path: Path, shard_images_dir: Path, shard_masks_dir: Path
):
    img = cv.imread(str(image_path))
    _, w = img.shape[:2]
    assert w % 3 == 0, f"Image width is not divisible by 3: {image_path=}, {img.shape=}"

    image = img[:, : w // 3]
    mask = img[:, 2 * w // 3 :]
    assert (
        image.shape == mask.shape
    ), f"Image and mask shapes do not match: {image.shape=}, {mask.shape=}"
    mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)

    cv.imwrite(str(shard_images_dir / image_path.name), image)
    cv.imwrite(str(shard_masks_dir / image_path.name), mask)
    image_path.unlink()


def process_dataset(ds: Path):
    images_dir = ds / "images"
    masks_dir = ds / "masks"
    labels_file = ds / "labels.json"

    if not images_dir.exists() or not labels_file.exists():
        raise FileNotFoundError(
            f"Dataset '{ds.name}' is missing 'images' directory or 'labels.json' file."
        )

    image_files = get_image_files(images_dir)
    total_images = len(image_files)

    if total_images == 0:
        raise ValueError(f"Dataset '{ds.name}' contains no images.")

    num_shards = math.ceil(total_images / SHARD_SIZE)

    for shard_idx in range(num_shards):
        start_idx = shard_idx * SHARD_SIZE
        end_idx = min(start_idx + SHARD_SIZE, total_images)
        shard_images = image_files[start_idx:end_idx]

        shard_images_dir = images_dir / f"{shard_idx:05d}"
        shard_images_dir.mkdir(exist_ok=True)

        shard_masks_dir = masks_dir / f"{shard_idx:05d}"
        if RENDER_MASK:
            shard_masks_dir.mkdir(parents=True, exist_ok=True)

        for image_path in shard_images:
            if RENDER_MASK:
                split_on_image_and_mask(image_path, shard_images_dir, shard_masks_dir)
            else:
                new_image_path = shard_images_dir / image_path.name
                image_path.rename(new_image_path)

    archive_path = ds.parent / f"{ds.name}.zip"
    create_archive(ds, archive_path)


@click.command()
@click.argument('datasets', nargs=-1, required=False)
@click.option(
    '--input-dir',
    '-i',
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    default=Path('tlr/output'),
)
def main(datasets, input_dir: Path):
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    dataset_paths = [p for p in input_dir.iterdir() if p.is_dir()]
    if datasets:
        for ds in datasets:
            if not (input_dir / ds).exists():
                raise FileNotFoundError(
                    f"Dataset '{ds}' does not exist in '{input_dir}'. Available datasets: {[p.name for p in dataset_paths]}"
                )
        dataset_paths = [input_dir / d for d in datasets if (input_dir / d).exists()]

    if not dataset_paths:
        raise FileNotFoundError("No datasets found to process.")

    for dataset_path in sorted(dataset_paths):
        process_dataset(dataset_path)


if __name__ == '__main__':
    main()
