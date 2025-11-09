import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from render_config import RENDER_MASK

# from make_per_language_char_set import latin_languages
latin_languages = ['en', 'de'] + ['bash', 'dots', 'math']

from text_renderer.config import (
    GeneratorCfg,
    NormPerspectiveTransformCfg,
    RenderCfg,
    SimpleTextColorCfg,
)
from text_renderer.corpus import *
from text_renderer.effect import *
from text_renderer.layout.extra_text_line import ExtraTextLineLayout
from text_renderer.layout.same_line import SameLineLayout

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
OUT_DIR = CURRENT_DIR / "output"
DATA_DIR = CURRENT_DIR
BG_DIR = DATA_DIR / "bg"
BG_SIMPLE_DIR = DATA_DIR / "bg_simple"
CHAR_DIR = DATA_DIR / "char"
FONT_DIR = DATA_DIR / "font"
FONT_LIST_DIR = DATA_DIR / "font_list"
FONT_LIST = FONT_LIST_DIR / "font_list.txt"
FONT_BLACKLIST = FONT_LIST_DIR / "font_blacklist.txt"
TEXT_DIR = DATA_DIR / "text"

FONT_SIZE = (30, 31)
CHAR_SPACING = (-0.1, 0.5)


def merge_fragile_and_robust_fonts():
    fragile_file = FONT_LIST_DIR / "fragile_fonts.txt"
    robust_file = FONT_LIST_DIR / "robust_fonts.txt"
    out_file = FONT_LIST_DIR / "fragile_and_robust_fonts.txt"

    fragile_fonts = []
    with open(fragile_file, 'r') as f:
        fragile_fonts = [line.strip() for line in f if line.strip()]

    robust_fonts = []
    with open(robust_file, 'r') as f:
        robust_fonts = [line.strip() for line in f if line.strip()]

    all_fonts = sorted(set(fragile_fonts + robust_fonts))
    with open(out_file, 'w') as f:
        for font in all_fonts:
            f.write(font + '\n')


merge_fragile_and_robust_fonts()


def get_font_blacklist():
    if not FONT_BLACKLIST.exists():
        return []

    with open(FONT_BLACKLIST, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def create_font_list():
    FONT_LIST_DIR.mkdir(exist_ok=True)

    font_blacklist = get_font_blacklist()
    counter = 0
    with open(FONT_LIST, 'w') as f:
        for font_file in FONT_DIR.glob('*'):
            if font_file.name.startswith('Noto'):
                continue
            if "SC" in font_file.name:  # skip small caps fonts
                continue
            if font_file.name in font_blacklist:
                continue

            if font_file.is_file():
                f.write(font_file.name + '\n')
            counter += 1
            if counter == 300:  # DELETE for more fonts
                break


# create_font_list()

perspective_transform = NormPerspectiveTransformCfg(20, 20, 1.5)
LATIN_TEXTS = [TEXT_DIR / f"{lang_code}_text.txt" for lang_code in latin_languages]


def get_num_images(num_images, part):
    return max(1, round(num_images * part))


def base_cfg(
    name: str,
    corpus,
    corpus_effects=None,
    layout_effects=None,
    layout=None,
    num_images=50,
    bg_dir=BG_SIMPLE_DIR,
):
    return GeneratorCfg(
        num_image=num_images,
        save_dir=OUT_DIR / name,
        render_cfg=RenderCfg(
            bg_dir=bg_dir,
            perspective_transform=perspective_transform,
            gray=False,
            layout_effects=layout_effects,
            render_effects=Effects(
                [
                    Line(0.5, color_cfg=SimpleTextColorCfg()),
                    TLR(),
                ]
            ),
            layout=layout,
            corpus=corpus,
            corpus_effects=corpus_effects,
            height=40,
            return_bg_and_mask=RENDER_MASK,
        ),
    )


def get_test_corpus(font_list_file=FONT_LIST):
    return EnumCorpus(
        EnumCorpusCfg(
            text_paths=[TEXT_DIR / "test_text.txt"],
            filter_by_chars=True,
            chars_file=CHAR_DIR / "test.txt",
            font_dir=FONT_DIR,
            font_list_file=font_list_file,
            font_size=FONT_SIZE,
        ),
    )


def get_slice_corpus(font_list_file, length=(1, 30)):
    return CharCorpus(
        CharCorpusCfg(
            text_paths=LATIN_TEXTS,
            filter_by_chars=True,
            chars_file=CHAR_DIR / f"latin.txt",
            length=length,
            char_spacing=CHAR_SPACING,
            font_dir=FONT_DIR,
            font_list_file=font_list_file,
            font_size=FONT_SIZE,
        ),
    )


def get_word_corpus(font_list_file, num_word=(1, 5)):
    return WordCorpus(
        WordCorpusCfg(
            text_paths=LATIN_TEXTS,
            filter_by_chars=True,
            chars_file=CHAR_DIR / f"latin.txt",
            num_word=num_word,
            char_spacing=CHAR_SPACING,
            font_dir=FONT_DIR,
            font_list_file=font_list_file,
            font_size=FONT_SIZE,
        ),
    )


def get_rand_corpus(font_list_file, length=(3, 30)):
    return RandCorpus(
        RandCorpusCfg(
            chars_file=CHAR_DIR / f"latin.txt",
            length=length,
            char_spacing=CHAR_SPACING,
            font_dir=FONT_DIR,
            font_list_file=font_list_file,
            font_size=FONT_SIZE,
        ),
    )


CORPUS_FUNCTIONS = {
    'slice': (0.5, get_slice_corpus),
    'word': (0.5, get_word_corpus),
    # 'rand': (0.1, get_rand_corpus),
}


def generate_basic_configs(num_images):
    configs = []

    corpuses = {
        k: (w, func(FONT_LIST_DIR / 'fragile_and_robust_fonts.txt'))
        for k, (w, func) in CORPUS_FUNCTIONS.items()
    }
    for corpus_name, (w, corpus) in corpuses.items():
        configs.append(
            base_cfg(
                f"latin_simple_{corpus_name}_corpus",
                corpus=corpus,
                layout_effects=Effects(
                    [
                        Padding(p=0.9, w_ratio=[0.1, 0.2], h_ratio=[0.1, 0.2]),
                    ]
                ),
                num_images=get_num_images(num_images, w / 2),
            )
        )

        configs.append(
            base_cfg(
                f"latin_basic_{corpus_name}_corpus",
                corpus=corpus,
                layout_effects=Effects(
                    [
                        OneOf(
                            [
                                DropoutRand(),
                                DropoutVertical(thickness=1),
                                DropoutHorizontal(thickness=1),
                            ]
                        ),
                        Padding(p=0.9, w_ratio=[0.1, 0.2], h_ratio=[0.1, 0.2]),
                    ]
                ),
                num_images=get_num_images(num_images, w / 2),
            )
        )

    return configs


def generate_mixed_style_configs(num_images):
    configs = []

    corpuses = {
        k: (w, func(FONT_LIST_DIR / 'fragile_and_robust_fonts.txt'))
        for k, (w, func) in CORPUS_FUNCTIONS.items()
    }
    for corpus_name, (w, corpus) in corpuses.items():
        configs.append(
            base_cfg(
                f"latin_mixed_style_{corpus_name}_corpus",
                layout=SameLineLayout(h_spacing=(0, 0.01)),
                corpus=[corpus, corpus],
                corpus_effects=[
                    Effects([Padding(p=0.3, w_ratio=[0, 0.01]), DropoutRand(p=0.2)]),
                    Effects([Padding(p=0.3, w_ratio=[0, 0.01]), DropoutRand(p=0.2)]),
                ],
                num_images=get_num_images(num_images, w),
            )
        )

    return configs


def generate_with_adjacent_line_configs(num_images):
    configs = []

    corpuses = {
        k: (w, func(FONT_LIST_DIR / 'fragile_and_robust_fonts.txt'))
        for k, (w, func) in CORPUS_FUNCTIONS.items()
    }
    for corpus_name, (w, corpus) in corpuses.items():
        configs.append(
            base_cfg(
                f"latin_adjacent_line_{corpus_name}_corpus",
                layout=ExtraTextLineLayout(bottom_prob=0.5),
                corpus=[corpus, corpus],
                corpus_effects=[
                    Effects([Padding(p=0.9), DropoutRand(p=0.2)]),
                    NoEffects(),
                ],
                num_images=get_num_images(num_images, w),
            )
        )

    return configs


def generate_hard_bg_configs(num_images):
    configs = []

    corpuses = {
        k: (w, func(FONT_LIST_DIR / 'robust_fonts.txt'))
        for k, (w, func) in CORPUS_FUNCTIONS.items()
    }
    for corpus_name, (w, corpus) in corpuses.items():
        configs.append(
            base_cfg(
                f"latin_hard_bg_{corpus_name}_corpus",
                corpus=corpus,
                corpus_effects=Effects(
                    [
                        DropoutRand(p=0.5),
                        Padding(p=0.9, w_ratio=[0.1, 0.2], h_ratio=[0.1, 0.2]),
                    ]
                ),
                bg_dir=BG_DIR,
                num_images=get_num_images(num_images, w),
            )
        )

    return configs


def generate_extreme_fonts_configs(num_images):
    configs = []

    corpuses = {
        k: (w, func(FONT_LIST_DIR / 'extreme_fonts.txt'))
        for k, (w, func) in CORPUS_FUNCTIONS.items()
    }
    for corpus_name, (w, corpus) in corpuses.items():
        configs.append(
            base_cfg(
                f"latin_simple_extreme_fonts_{corpus_name}_corpus",
                corpus=corpus,
                layout_effects=Effects(
                    [
                        Padding(p=0.9, w_ratio=[0.1, 0.2], h_ratio=[0.1, 0.2]),
                    ]
                ),
                num_images=get_num_images(num_images, w / 2),
            )
        )

        configs.append(
            base_cfg(
                f"latin_basic_extreme_fonts_{corpus_name}_corpus",
                corpus=corpus,
                layout_effects=Effects(
                    [
                        OneOf(
                            [
                                DropoutRand(),
                                DropoutVertical(thickness=1),
                                DropoutHorizontal(thickness=1),
                            ]
                        ),
                        Padding(p=0.9, w_ratio=[0.1, 0.2], h_ratio=[0.1, 0.2]),
                    ]
                ),
                num_images=get_num_images(num_images, w / 2),
            )
        )

    return configs


def generate_validation_configs(num_images):
    configs = []

    corpus = get_word_corpus(FONT_LIST_DIR / 'fragile_and_robust_fonts.txt')
    ds_name = 'validation'
    w = 0.25  # part of num_images per config

    configs.append(
        base_cfg(
            ds_name,
            corpus=corpus,
            layout_effects=Effects(
                [
                    OneOf(
                        [
                            DropoutRand(),
                            DropoutVertical(thickness=1),
                            DropoutHorizontal(thickness=1),
                        ]
                    ),
                    Padding(p=0.9, w_ratio=[0.1, 0.2], h_ratio=[0.1, 0.2]),
                ]
            ),
            num_images=get_num_images(num_images, w),
        )
    )

    configs.append(
        base_cfg(
            ds_name,
            layout=SameLineLayout(h_spacing=(0, 0.01)),
            corpus=[corpus, corpus],
            corpus_effects=[
                Effects([Padding(p=0.3, w_ratio=[0, 0.01]), DropoutRand(p=0.2)]),
                Effects([Padding(p=0.3, w_ratio=[0, 0.01]), DropoutRand(p=0.2)]),
            ],
            num_images=get_num_images(num_images, w),
        )
    )

    configs.append(
        base_cfg(
            ds_name,
            layout=ExtraTextLineLayout(bottom_prob=0.5),
            corpus=[corpus, corpus],
            corpus_effects=[
                Effects([Padding(p=0.9), DropoutRand(p=0.2)]),
                NoEffects(),
            ],
            num_images=get_num_images(num_images, w),
        )
    )

    corpus = get_word_corpus(FONT_LIST_DIR / 'robust_fonts.txt')
    configs.append(
        base_cfg(
            ds_name,
            corpus=corpus,
            corpus_effects=Effects(
                [
                    DropoutRand(p=0.5),
                    Padding(p=0.9, w_ratio=[0.1, 0.2], h_ratio=[0.1, 0.2]),
                ]
            ),
            bg_dir=BG_DIR,
            num_images=get_num_images(num_images, w),
        )
    )

    return configs


def generate_per_font_configs():
    configs = []

    font_list = FONT_LIST_DIR / 'fragile_and_robust_fonts.txt'
    with open(font_list, 'r') as f:
        font_files = [line.strip() for line in f if line.strip()]

    for i, font_name in enumerate(font_files):
        font_file = Path(font_name)
        if font_file.name in get_font_blacklist():
            continue

        font_list_file = FONT_LIST_DIR / f'tmp.txt'
        with open(font_list_file, 'w') as f:
            f.write(font_file.name + '\n')

        try:
            configs.append(
                base_cfg(
                    f"font_{i}_{font_file.stem}",
                    corpus=get_test_corpus(font_list_file=font_list_file),
                    num_images=1,
                )
            )
        except Exception as e:
            print(f"Error with font {font_file}: {e}")
            continue

    return configs


def generate_all_configs():
    num_images = 10**6

    all_configs = []
    all_configs.extend(generate_basic_configs(get_num_images(num_images, 0.4)))
    # all_configs.extend(generate_mixed_style_configs(get_num_images(num_images, 0.3)))
    all_configs.extend(
        generate_with_adjacent_line_configs(get_num_images(num_images, 0.4))
    )
    all_configs.extend(generate_hard_bg_configs(get_num_images(num_images, 0.2)))
    # all_configs.extend(generate_extreme_fonts_configs(get_num_images(num_images, 0.05)))

    all_configs.extend(generate_validation_configs(100))

    # debug per font
    # all_configs.extend(generate_per_font_configs())

    return all_configs


configs = generate_all_configs()
