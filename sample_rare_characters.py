import os
import random
from pathlib import Path
from typing import List

import numpy as np

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
TEXT_DIR = CURRENT_DIR / "tlr" / "text"
LANGUAGES = (
    ['en', 'de'] + ['bash', 'dots', 'email', 'math', 'url'] + ['it', 'pl', 'ro', 'tr']
)

SRC_TEXT_FILES = [TEXT_DIR / f'{lang}_text.txt' for lang in LANGUAGES]

DST_FILE = CURRENT_DIR / "tlr" / "text" / "rare_characters_samples.txt"

SAMPLE_MIN_LENGTH = 1
SAMPLE_MAX_LENGTH = 100
RARE_CHARACTERS = {
    'j': 2000,
    '\'': 2000,
    'ü': 2000,
    '8': 2000,
    'V': 2000,
    '3': 3000,
    'Z': 3000,
    '5': 3000,
    'Y': 3000,
    '4': 3000,
    ':': 3000,
    '7': 5000,
    '6': 5000,
    '"': 3000,
    '/': 3000,
    'J': 5000,
    'ă': 5000,
    '=': 5000,
    '•': 5000,
    'ş': 10000,
    'ö': 10000,
    'x': 10000,
    'ó': 10000,
    'ä': 10000,
    'ę': 10000,
    'ą': 10000,
    'ç': 10000,
    'ğ': 10000,
    'q': 10000,
    ';': 10000,
    '@': 10000,
    'ș': 11000,
    'Ü': 11000,
    'ț': 11000,
    'î': 2660,
    'ż': 11000,
    'ś': 11000,
    '[': 11000,
    '_': 11000,
    ']': 11000,
    '^': 11000,
    '?': 11000,
    '|': 11000,
    'X': 13000,
    '{': 13000,
    '}': 13000,
    'Ş': 13000,
    '&': 13000,
    'â': 13000,
    'Ö': 13000,
    'ß': 10000,
    'è': 13000,
    '+': 5000,
    'Ă': 10000,
    'ń': 13000,
    'à': 13000,
    'Ç': 13000,
    'Q': 13000,
    '%': 13000,
    'é': 13000,
    'ć': 13000,
    'İ': 13000,
    'Î': 13000,
    'Ğ': 13000,
    'Ä': 13000,
    '$': 13000,
    'Ó': 13000,
    'Ą': 13000,
    'Ę': 13000,
    'Ś': 13000,
    'Ș': 13000,
    'ò': 13000,
    'Ż': 13000,
    'Ț': 13000,
    'È': 13000,
    'ź': 13000,
    'ù': 13000,
    'Â': 13000,
    'ì': 13000,
    '°': 13000,
    '£': 13000,
    'É': 13000,
    '¢': 13000,
    '!': 13000,
    '€': 13000,
    'À': 13000,
    'Ń': 13000,
    'Ć': 13000,
    '\\': 13000,
    'Ò': 13000,
    '#': 13000,
    'Ù': 13000,
    'Ź': 13000,
    'Ì': 13000,
}


def extract_text_snippet(text: str, char_pos: int, min_len: int, max_len: int) -> str:
    snippet_length = random.randint(min_len, max_len - 1)
    shift = random.randint(0, snippet_length)

    start_pos = max(0, char_pos - shift)
    end_pos = min(len(text), start_pos + snippet_length)

    snippet = text[start_pos : end_pos + 1].replace('\n', ' ').replace('\r', '').strip()
    assert len(snippet) > 0
    assert (
        text[char_pos] in snippet
    ), f'{char_pos=}, {text[char_pos]=}, {start_pos=}, {end_pos=}, {snippet=}, {text[start_pos:end_pos]=}'

    return snippet


def find_samples_for_character(
    text: str, target_char: str, num_samples: int
) -> List[str]:
    samples = []
    positions = []

    for i, char in enumerate(text):
        if char == target_char:
            positions.append(i)

    indices = np.random.choice(np.arange(len(positions)), num_samples)
    positions = [positions[i] for i in indices]

    for pos in positions:
        snippet = extract_text_snippet(text, pos, SAMPLE_MIN_LENGTH, SAMPLE_MAX_LENGTH)
        samples.append(snippet)

    return samples


def main():
    assert SAMPLE_MAX_LENGTH > SAMPLE_MIN_LENGTH
    texts = []
    for file_path in SRC_TEXT_FILES:
        if file_path.exists():
            try:
                text = file_path.read_text(encoding='utf-8')
                texts.append(text)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    assert len(texts) > 0, "No texts loaded from source files."
    text = '\n'.join(texts)

    all_samples = []

    for char, num_samples in RARE_CHARACTERS.items():
        samples = find_samples_for_character(text, char, num_samples)
        all_samples.extend(samples)

    DST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DST_FILE, 'w', encoding='utf-8') as f:
        for sample in all_samples:
            f.write(sample + '\n')


if __name__ == "__main__":
    main()
