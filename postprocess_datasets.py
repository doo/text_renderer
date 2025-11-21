#!/Users/igoreremin/.envs/text_renderer/bin/python

import json
import math
import os
import zipfile
from pathlib import Path
from typing import List

import click
import cv2 as cv
import numpy as np
from tqdm import tqdm

from render_config import RENDER_MASK, TARGET_HEIGHT

SHARD_SIZE = 1000


def get_image_files(images_dir: Path) -> List[Path]:
    return sorted(images_dir.glob("*.jpg"))


def create_archive(dataset_dir: Path, archive_path: Path):
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(dataset_dir):
            for file in files:
                file_path = Path(root) / file
                arc_name = file_path.relative_to(dataset_dir)
                zf.write(file_path, arc_name)


def dithering(img: np.ndarray, threshold_map_size: int = 4) -> np.ndarray:
    """Apply ordered dithering using a threshold map.

    Args:
        img: Input grayscale image as numpy array
        threshold_map_size: Size of the Bayer threshold map (4 or 8)

    Returns:
        Dithered image as numpy array
    """
    # Define Bayer threshold maps
    bayer_maps = {
        4: np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]])
        * 16,
        8: np.array(
            [
                [0, 32, 8, 40, 2, 34, 10, 42],
                [48, 16, 56, 24, 50, 18, 58, 26],
                [12, 44, 4, 36, 14, 46, 6, 38],
                [60, 28, 52, 20, 62, 30, 54, 22],
                [3, 35, 11, 43, 1, 33, 9, 41],
                [51, 19, 59, 27, 49, 17, 57, 25],
                [15, 47, 7, 39, 13, 45, 5, 37],
                [63, 31, 55, 23, 61, 29, 53, 21],
            ]
        )
        * 4,
    }

    threshold_map = bayer_maps.get(threshold_map_size, bayer_maps[4])
    map_height, map_width = threshold_map.shape
    height, width = img.shape

    # Create tiled threshold map
    tiles_y = (height + map_height - 1) // map_height
    tiles_x = (width + map_width - 1) // map_width
    tiled_map = np.tile(threshold_map, (tiles_y, tiles_x))[:height, :width]

    # Apply dithering
    dithered = np.where(img > tiled_map, 255, 0).astype(np.uint8)
    return dithered


def post_generation_augmentation(image_files: list[Path], label_file: Path):
    if RENDER_MASK:
        raise NotImplementedError(
            "Post-generation augmentation for masks is not implemented."
        )

    with open(label_file, 'r') as f:
        label_info = json.load(f)

    for img_file in tqdm(image_files, desc="Post-generation augmentation"):
        img = cv.imread(str(img_file))
        chars = label_info['chars'][img_file.stem]

        p = np.random.rand()
        if p < 0.3:
            # crop augmentation
            top_padding = 0
            bottom_padding = 0
            if np.random.rand() < 0.5:
                top_padding = round(np.random.uniform(0, 0.3) * TARGET_HEIGHT)
            if np.random.rand() < 0.5:
                bottom_padding = round(np.random.uniform(0, 0.5) * TARGET_HEIGHT)
            img = img[top_padding : img.shape[0] - bottom_padding, :]
            scale = TARGET_HEIGHT / img.shape[0]

            for ch in chars:
                if 'bbox' not in ch:
                    continue

                for corner in ch['bbox']:
                    corner[1] -= top_padding
                    corner[0] *= scale
                    corner[1] *= scale

            img = cv.resize(
                img,
                None,
                fx=scale,
                fy=scale,
                interpolation=cv.INTER_LINEAR,
            )
        elif p < 0.6:
            # resize augmentation
            scale = np.random.uniform(0.25, 1.0)
            shape = img.shape[:2]
            img = cv.resize(
                img, None, fx=scale, fy=scale, interpolation=cv.INTER_LINEAR
            )
            img = cv.resize(img, shape[::-1], interpolation=cv.INTER_LINEAR)
        elif p < 0.8:
            # squeeze/stretch augmentation
            img_width = img.shape[1]
            if img_width > 20:
                src_position = np.random.uniform(0.3, 0.7)
                dst_position = (
                    np.random.uniform(0.5 * src_position, src_position)
                    if np.random.rand() < 0.5
                    else np.random.uniform(
                        src_position, src_position + 0.5 * (1 - src_position)
                    )
                )

                x = round(img_width * src_position)
                left_part = img[:, :x]
                right_part = img[:, x:]

                dst_left_w = round(img_width * dst_position)
                dst_right_w = img_width - dst_left_w

                left_scale = dst_left_w / x
                right_scale = dst_right_w / (img_width - x)
                for ch in chars:
                    if 'bbox' not in ch:
                        continue

                    for corner in ch['bbox']:
                        if corner[0] <= x:
                            corner[0] *= left_scale
                        elif corner[0] > x:
                            corner[0] = (corner[0] - x) * right_scale + dst_left_w

                left_part = cv.resize(
                    left_part,
                    (dst_left_w, left_part.shape[0]),
                    interpolation=cv.INTER_LINEAR,
                )
                right_part = cv.resize(
                    right_part,
                    (dst_right_w, right_part.shape[0]),
                    interpolation=cv.INTER_LINEAR,
                )
                img[:, :dst_left_w] = left_part
                img[:, dst_left_w:] = right_part
        elif p < 0.9:
            # dithering augmentation
            if len(img.shape) == 3:
                img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            img = dithering(img, threshold_map_size=np.random.choice([4, 8]))
            if np.random.rand() < 0.5:
                kernel_size = np.random.choice([3, 5, 7])
                img = cv.GaussianBlur(img, (kernel_size, kernel_size), 0)

        cv.imwrite(str(img_file), img)
        label_info['sizes'][img_file.stem] = [img.shape[1], img.shape[0]]
        label_info['chars'][img_file.stem] = chars

    with open(label_file, 'w') as f:
        json.dump(label_info, f, indent=4)


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

    post_generation_augmentation(image_files, labels_file)

    if total_images == 0:
        raise ValueError(f"Dataset '{ds.name}' contains no images.")

    num_shards = math.ceil(total_images / SHARD_SIZE)

    for shard_idx in range(num_shards):
        start_idx = shard_idx * SHARD_SIZE
        end_idx = min(start_idx + SHARD_SIZE, total_images)
        shard_images = image_files[start_idx:end_idx]

        shard_images_dir = images_dir / f"{shard_idx:05d}"
        shard_images_dir.mkdir(exist_ok=True)

        if RENDER_MASK and masks_dir.exists():
            shard_masks_dir = masks_dir / f"{shard_idx:05d}"
            shard_masks_dir.mkdir(parents=True, exist_ok=True)

        for image_path in shard_images:
            new_image_path = shard_images_dir / image_path.name
            image_path.rename(new_image_path)

            if RENDER_MASK and masks_dir.exists():
                mask_filename = image_path.stem + ".png"
                mask_path = masks_dir / mask_filename
                if mask_path.exists():
                    new_mask_path = shard_masks_dir / mask_filename
                    mask_path.rename(new_mask_path)

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
