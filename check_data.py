from collections import Counter
from pathlib import Path

from fontTools.ttLib import TTFont

from make_per_language_char_set import languages


def load_character_set(language):
    char_file = Path("tlr/char") / f"{language}.txt"
    if not char_file.exists():
        return set()

    with open(char_file, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())


def load_text_content(language):
    text_file = Path("tlr/text") / f"{language}_text.txt"
    if not text_file.exists():
        return ""

    with open(text_file, 'r', encoding='utf-8') as f:
        return f.read()


def get_font_supported_chars(font_path):
    try:
        font = TTFont(font_path)
        cmap = font.getBestCmap()
        return set(chr(unicode_val) for unicode_val in cmap.keys())
    except Exception as e:
        print(f"Error reading font {font_path}: {e}")
        return set()


def get_font_list():
    font_list_file = Path("tlr/font_list/font_list.txt")
    if not font_list_file.exists():
        return []

    with open(font_list_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def analyze_language(language):
    char_set = load_character_set(language)
    text_content = load_text_content(language)

    if not char_set:
        print(f"Language {language}: No character set found")
        return

    if not text_content:
        print(f"Language {language}: No text content found")
        return

    text_chars = set(text_content)
    char_counter = Counter(text_content)

    unused_chars = char_set - text_chars
    missing_chars = text_chars - char_set

    print(f"\nLanguage: {language}")

    if unused_chars:
        print(f"Unused chars ({len(unused_chars)}): {sorted(unused_chars)}")

    if missing_chars:
        print(f"Out of alphabet chars ({len(missing_chars)}): {sorted(missing_chars)}")

    # print("Character distribution (top 20):")
    # for char, count in char_counter.most_common(20):
    #     if char in ['\n', ' ']:
    #         continue
    #     print(f"  '{char}': {count}")


def analyze_font_support(language):
    char_set = load_character_set(language)
    text_content = load_text_content(language)

    if not char_set:
        return

    if not text_content:
        return

    text_chars = set(text_content) - {'\n'}
    font_list = get_font_list()

    for font_name in font_list:
        font_path = Path("tlr/font") / font_name
        if not font_path.exists():
            continue

        supported_chars = get_font_supported_chars(font_path)

        unsupported_from_set = char_set - supported_chars
        unsupported_from_text = text_chars - supported_chars

        if unsupported_from_set or unsupported_from_text:
            print(f"{font_name}:")

            if unsupported_from_set:
                print(
                    f"  Unsupported alphabet chars ({len(unsupported_from_set)}): {sorted(unsupported_from_set)}"
                )

            if unsupported_from_text:
                print(
                    f"  Unsupported from text ({len(unsupported_from_text)}): {sorted(unsupported_from_text)}"
                )


def main():
    for language in languages:
        analyze_language(language)
        analyze_font_support(language)


if __name__ == "__main__":
    main()
