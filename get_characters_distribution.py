import os
from collections import Counter
from pathlib import Path

CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
TEXT_DIR = CURRENT_DIR / "tlr" / "text"
LANGUAGES = (
    ['en', 'de'] + ['bash', 'dots', 'email', 'math', 'url'] + ['it', 'pl', 'ro', 'tr']
)
SOURCE_FILES = [TEXT_DIR / f'{lang}_text.txt' for lang in LANGUAGES]
ALLOWE_CHARS_FILE = CURRENT_DIR / 'tlr' / 'char' / 'latin.txt'
mapping = {
    '¨': '"',  # DIAERESIS                                --> QUOTATION MARK
    '´': '\'',  # ACUTE ACCENT                             --> APOSTROPHE
    'µ': 'μ',  # MICRO SIGN                               --> GREEK SMALL LETTER MU
    '·': '•',  # MIDDLE DOT                               --> BULLET
    'º': '°',  # MASCULINE ORDINAL INDICATOR              --> DEGREE SIGN
    '×': 'x',  # MULTIPLICATION SIGN                      --> LATIN SMALL LETTER X
    'Ø': '0',  # LATIN CAPITAL LETTER O WITH STROKE       --> DIGIT ZERO
    'Đ': 'Ð',  # LATIN CAPITAL LETTER D WITH STROKE       --> LATIN CAPITAL LETTER ETH
    'Ɖ': 'Ð',  # LATIN CAPITAL LETTER AFRICAN D           --> LATIN CAPITAL LETTER ETH
    'đ': 'ð',  # LATIN SMALL LETTER D WITH STROKE         --> LATIN SMALL LETTER ETH
    'Ŀ': 'L',  # LATIN CAPITAL LETTER L WITH MIDDLE DOT   --> LATIN CAPITAL LETTER L
    'Ƒ': 'F',  # LATIN CAPITAL LETTER F WITH HOOK         --> LATIN CAPITAL LETTER F
    'ƒ': 'f',  # LATIN SMALL LETTER F WITH HOOK           --> LATIN SMALL LETTER F
    'ɓ': 'b',  # LATIN SMALL LETTER B WITH HOOK           --> LATIN SMALL LETTER B
    'ʹ': '\'',  # MODIFIER LETTER PRIME                    --> APOSTROPHE
    'ʻ': '\'',  # MODIFIER LETTER TURNED COMMA             --> APOSTROPHE
    'ʼ': '\'',  # MODIFIER LETTER APOSTROPHE               --> APOSTROPHE
    'ˆ': '^',  # MODIFIER LETTER CIRCUMFLEX ACCENT        --> CIRCUMFLEX ACCENT
    'ˊ': '\'',  # MODIFIER LETTER ACUTE ACCENT             --> APOSTROPHE
    'ˋ': '\'',  # MODIFIER LETTER GRAVE ACCENT             --> APOSTROPHE
    '˚': '°',  # RING ABOVE                               --> DEGREE SIGN
    '˜': '~',  # SMALL TILDE                              --> TILDE
    '͵': ',',  # GREEK LOWER NUMERAL SIGN                 --> COMMA
    'Α': 'A',  # GREEK CAPITAL LETTER ALPHA               --> LATIN CAPITAL LETTER A
    'Β': 'B',  # GREEK CAPITAL LETTER BETA                --> LATIN CAPITAL LETTER B
    'Ε': 'E',  # GREEK CAPITAL LETTER EPSILON             --> LATIN CAPITAL LETTER E
    'Ζ': 'Z',  # GREEK CAPITAL LETTER ZETA                --> LATIN CAPITAL LETTER Z
    'Η': 'H',  # GREEK CAPITAL LETTER ETA                 --> LATIN CAPITAL LETTER H
    'Ι': 'I',  # GREEK CAPITAL LETTER IOTA                --> LATIN CAPITAL LETTER I
    'Κ': 'K',  # GREEK CAPITAL LETTER KAPPA               --> LATIN CAPITAL LETTER K
    'Μ': 'M',  # GREEK CAPITAL LETTER MU                  --> LATIN CAPITAL LETTER M
    'Ν': 'N',  # GREEK CAPITAL LETTER NU                  --> LATIN CAPITAL LETTER N
    'Ο': 'O',  # GREEK CAPITAL LETTER OMICRON             --> LATIN CAPITAL LETTER O
    'Ρ': 'P',  # GREEK CAPITAL LETTER RHO                 --> LATIN CAPITAL LETTER P
    'Τ': 'T',  # GREEK CAPITAL LETTER TAU                 --> LATIN CAPITAL LETTER T
    'Υ': 'Y',  # GREEK CAPITAL LETTER UPSILON             --> LATIN CAPITAL LETTER Y
    'Χ': 'X',  # GREEK CAPITAL LETTER CHI                 --> LATIN CAPITAL LETTER X
    'Ϊ': 'Ï',  # GREEK CAPITAL LETTER IOTA WITH DIALYTIKA --> LATIN CAPITAL LETTER I WITH DIAERESIS
    'ΰ': 'ǘ',  # GREEK SMALL LETTER UPSILON WITH DIALYTIKA AND TONOS --> LATIN SMALL LETTER U WITH DIAERESIS AND ACUTE
    'ν': 'v',  # GREEK SMALL LETTER NU                    --> LATIN SMALL LETTER V
    'ο': 'o',  # GREEK SMALL LETTER OMICRON               --> LATIN SMALL LETTER O
    'υ': 'u',  # GREEK SMALL LETTER UPSILON               --> LATIN SMALL LETTER U
    'ϋ': 'ü',  # GREEK SMALL LETTER UPSILON WITH DIALYTIKA --> LATIN SMALL LETTER U WITH DIAERESIS
    'ό': 'ó',  # GREEK SMALL LETTER OMICRON WITH TONOS    --> LATIN SMALL LETTER O WITH ACUTE
    'ύ': 'ú',  # GREEK SMALL LETTER UPSILON WITH TONOS    --> LATIN SMALL LETTER U WITH ACUTE
    'Ё': 'Ë',  # CYRILLIC CAPITAL LETTER IO               --> LATIN CAPITAL LETTER E WITH DIAERESIS
    'І': 'I',  # CYRILLIC CAPITAL LETTER BYELORUSSIAN-UKRAINIAN I --> LATIN CAPITAL LETTER I
    'Ј': 'J',  # CYRILLIC CAPITAL LETTER JE               --> LATIN CAPITAL LETTER J
    'Ќ': 'Ḱ',  # CYRILLIC CAPITAL LETTER KJE              --> LATIN CAPITAL LETTER K WITH ACUTE
    'А': 'A',  # CYRILLIC CAPITAL LETTER A                --> LATIN CAPITAL LETTER A
    'В': 'B',  # CYRILLIC CAPITAL LETTER VE               --> LATIN CAPITAL LETTER B
    'Е': 'E',  # CYRILLIC CAPITAL LETTER IE               --> LATIN CAPITAL LETTER E
    'З': '3',  # CYRILLIC CAPITAL LETTER ZE               --> DIGIT THREE
    'К': 'K',  # CYRILLIC CAPITAL LETTER KA               --> LATIN CAPITAL LETTER K
    'М': 'M',  # CYRILLIC CAPITAL LETTER EM               --> LATIN CAPITAL LETTER M
    'Н': 'H',  # CYRILLIC CAPITAL LETTER EN               --> LATIN CAPITAL LETTER H
    'О': 'O',  # CYRILLIC CAPITAL LETTER O                --> LATIN CAPITAL LETTER O
    'Р': 'P',  # CYRILLIC CAPITAL LETTER ER               --> LATIN CAPITAL LETTER P
    'С': 'C',  # CYRILLIC CAPITAL LETTER ES               --> LATIN CAPITAL LETTER C
    'Т': 'T',  # CYRILLIC CAPITAL LETTER TE               --> LATIN CAPITAL LETTER T
    'а': 'a',  # CYRILLIC SMALL LETTER A                  --> LATIN SMALL LETTER A
    'е': 'e',  # CYRILLIC SMALL LETTER IE                 --> LATIN SMALL LETTER E
    'о': 'o',  # CYRILLIC SMALL LETTER O                  --> LATIN SMALL LETTER O
    'р': 'p',  # CYRILLIC SMALL LETTER ER                 --> LATIN SMALL LETTER P
    'с': 'c',  # CYRILLIC SMALL LETTER ES                 --> LATIN SMALL LETTER C
    'у': 'y',  # CYRILLIC SMALL LETTER U                  --> LATIN SMALL LETTER Y
    'ё': 'ë',  # CYRILLIC SMALL LETTER IO                 --> LATIN SMALL LETTER E WITH DIAERESIS
    'і': 'i',  # CYRILLIC SMALL LETTER BYELORUSSIAN-UKRAINIAN I --> LATIN SMALL LETTER I
    'ї': 'ï',  # CYRILLIC SMALL LETTER YI                 --> LATIN SMALL LETTER I WITH DIAERESIS
    'ј': 'j',  # CYRILLIC SMALL LETTER JE                 --> LATIN SMALL LETTER J
    'Ү': 'Y',  # CYRILLIC CAPITAL LETTER STRAIGHT U       --> LATIN CAPITAL LETTER Y
    'ү': 'Y',  # CYRILLIC SMALL LETTER STRAIGHT U         --> LATIN CAPITAL LETTER Y
    'ӱ': 'ÿ',  # CYRILLIC SMALL LETTER U WITH DIAERESIS   --> LATIN SMALL LETTER Y WITH DIAERESIS
    'Տ': 'S',  # ARMENIAN CAPITAL LETTER TIWN             --> LATIN CAPITAL LETTER S
    'օ': 'o',  # ARMENIAN SMALL LETTER OH                 --> LATIN SMALL LETTER O
    '։': ':',  # ARMENIAN FULL STOP                       --> COLON
    '־': '-',  # HEBREW PUNCTUATION MAQAF                 --> HYPHEN-MINUS
    '܂': '.',  # SYRIAC SUBLINEAR FULL STOP               --> FULL STOP
    '܃': ':',  # SYRIAC SUPRALINEAR COLON                 --> COLON
    'ᵒ': 'o',  # MODIFIER LETTER SMALL O                  --> LATIN SMALL LETTER O
    'ὸ': 'ò',  # GREEK SMALL LETTER OMICRON WITH VARIA    --> LATIN SMALL LETTER O WITH GRAVE
    '᾽': '\'',  # GREEK KORONIS                            --> APOSTROPHE
    '᾿': '\'',  # GREEK PSILI                              --> APOSTROPHE
    '῾': '\'',  # GREEK DASIA                              --> APOSTROPHE
    '‐': '-',  # HYPHEN                                   --> HYPHEN-MINUS
    '‑': '-',  # NON-BREAKING HYPHEN                      --> HYPHEN-MINUS
    '‒': '-',  # FIGURE DASH                              --> HYPHEN-MINUS
    '–': '-',  # EN DASH                                  --> HYPHEN-MINUS
    '‘': '\'',  # LEFT SINGLE QUOTATION MARK               --> APOSTROPHE
    '’': '\'',  # RIGHT SINGLE QUOTATION MARK              --> APOSTROPHE
    '‚': ',',  # SINGLE LOW-9 QUOTATION MARK              --> COMMA
    '“': '"',  # LEFT DOUBLE QUOTATION MARK               --> QUOTATION MARK
    '”': '"',  # RIGHT DOUBLE QUOTATION MARK              --> QUOTATION MARK
    '․': '.',  # ONE DOT LEADER                           --> FULL STOP
    '…': '...',  # HORIZONTAL ELLIPSIS                      --> "..."
    '‧': '•',  # HYPHENATION POINT                        --> BULLET
    '′': '\'',  # PRIME                                    --> APOSTROPHE
    '‹': '<',  # SINGLE LEFT-POINTING ANGLE QUOTATION MARK --> LESS-THAN SIGN
    '›': '>',  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK --> GREATER-THAN SIGN
    '⁄': '/',  # FRACTION SLASH                           --> SOLIDUS
    'Ⅰ': 'I',  # ROMAN NUMERAL ONE                        --> LATIN CAPITAL LETTER I
    'Ⅹ': 'X',  # ROMAN NUMERAL TEN                        --> LATIN CAPITAL LETTER X
    '−': '-',  # MINUS SIGN                               --> HYPHEN-MINUS
    '∼': '~',  # TILDE OPERATOR                           --> TILDE
    '│': '|',  # BOX DRAWINGS LIGHT VERTICAL              --> VERTICAL LINE
    '▪': '■',  # BLACK SMALL SQUARE                       --> BLACK SQUARE
    '►': '▶',  # BLACK RIGHT-POINTING POINTER             --> BLACK RIGHT-POINTING TRIANGLE
    '◎': '•',  # BULLSEYE                                 --> BULLET
    '●': '•',  # BLACK CIRCLE                             --> BULLET
    '⚫': '•',  # BLACK CIRCLE EMOJI                      --> BULLET
    '❘': '|',  # LIGHT VERTICAL BAR                       --> VERTICAL LINE
    '❝': '"',  # HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT --> QUOTATION MARK
    '❞': '"',  # HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT --> QUOTATION MARK
    '〈': '<',  # LEFT ANGLE BRACKET                       --> LESS-THAN SIGN
    '〉': '>',  # RIGHT ANGLE BRACKET                      --> GREATER-THAN SIGN
    '｡': '.',  # HALFWIDTH IDEOGRAPHIC FULL STOP          --> FULL STOP
    '･': '.',  # HALFWIDTH KATAKANA MIDDLE DOT            --> FULL STOP
    '✔': '✓',  # HEAVY CHECK MARK                         --> CHECK MARK
    '`': '\'',  # GRAVE ACCENT                             --> APOSTROPHE
    '—': '-',  # EM DASH                                  --> HYPHEN-MINUS
    'Ⓒ': '©',  # CIRCLED LATIN CAPITAL LETTER C          --> COPYRIGHT SIGN
    'ⓒ': '©',  # CIRCLED LATIN SMALL LETTER C            --> COPYRIGHT SIGN
    'Ⓡ': '®',  # CIRCLED LATIN CAPITAL LETTER R          --> REGISTERED SIGN
    'Г': 'Γ',  # CYRILLIC CAPITAL LETTER GHE              --> GREEK CAPITAL LETTER GAMMA
    'П': 'Π',  # CYRILLIC CAPITAL LETTER PE               --> GREEK CAPITAL LETTER PI
    'х': 'x',  # CYRILLIC SMALL LETTER HA                 --> LATIN SMALL LETTER X
    'χ': 'x',  # GREEK SMALL LETTER CHI                    --> LATIN SMALL LETTER X
    'Х': 'X',  # CYRILLIC CAPITAL LETTER HA               --> LATIN CAPITAL LETTER X
    'к': 'k',  # CYRILLIC SMALL LETTER KA                 --> LATIN SMALL LETTER K
    'Ф': 'Φ',  # CYRILLIC CAPITAL LETTER EF               --> GREEK CAPITAL LETTER PHI
    'ф': 'φ',  # CYRILLIC SMALL LETTER EF                 --> GREEK SMALL LETTER PHI
}

TRANSLATION_TABLE = str.maketrans(mapping)


def main():
    allowed_chars = set()
    with open(ALLOWE_CHARS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            char = line.strip()
            allowed_chars.add(char)

    counter = Counter()
    for path in SOURCE_FILES:
        text = path.read_text(encoding='utf-8')
        counter.update(text)

    result = {}
    for char, count in counter.most_common():
        if char in mapping.keys():
            mapped_char = mapping[char]
            result[mapped_char] = result.get(mapped_char, 0) + count
        else:
            result[char] = result.get(char, 0) + count

    for char, count in result.items():
        if char not in allowed_chars:
            continue
        print(f'{char}: {count}')


if __name__ == "__main__":
    main()
