import string
from pathlib import Path

# ISO 639 language codes: https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes
latin_languages = [
    'bg',
    'cs',
    'da',
    'de',
    'el',
    'en',
    'es',
    'et',
    'fi',
    'fr',
    'ga',
    'hr',
    'hu',
    'it',
    'lt',
    'lv',
    'mt',
    'nl',
    'pl',
    'pt',
    'ro',
    'ru',
    'sk',
    'sl',
    'sv',
    'tr',
    'uk',
]
languages = latin_languages

blacklist = [
    b'\\u1c80',
    b'\\u1c81',
    b'\\u1c82',
    b'\\u1c83',
    b'\\u1c84',
    b'\\u1c85',
    b'\\u1c86',
]

punctuation = string.punctuation + '…'
currency = '€£$¢'
sign = '°±™¶§ⓇⒸⓒ®©'
other = '•●|│❘⋮—−–‒‑־'
common = ' ' + string.digits + punctuation + currency + sign + other


def get_exemplars(localeID, extype='main', option=2):
    import icu

    # Bitmask for options to apply to the exemplar pattern:
    #    0 -> retrieve the exemplar set as it is defined in the locale data
    #    2 -> retrieve a case-folded exemplar set (icu.USET_CASE_INSENSITIVE)
    #    4 -> retrieve a case-mapped exemplar set (icu.USET_ADD_CASE_MAPPINGS)
    option = option if option in [0, 2, 4] else 0
    extype = (
        extype.lower() if extype.lower() in ['main', 'auxiliary', 'index'] else None
    )
    localeID = localeID.replace('-', '_')
    if localeID in icu.Collator.getAvailableLocales():
        collator = icu.Collator.createInstance(icu.Locale(localeID))
    else:
        collator = icu.Collator.createInstance(icu.Locale.getRoot())
    # Type enumerations:
    #   icu.ULocaleDataExemplarSetType.ES_STANDARD -> 0
    #   icu.ULocaleDataExemplarSetType.ES_AUXILIARY -> 1
    #   icu.ULocaleDataExemplarSetType.ES_INDEX -> 2
    types = {'main': 0, 'auxiliary': 1, 'index': 2}
    type = types[extype]
    if localeID not in icu.Locale.getAvailableLocales():
        raise ValueError(f'Specified Locale not available in icu4c {icu.ICU_VERSION}')
    return sorted(
        icu.LocaleData(localeID).getExemplarSet(option, type), key=collator.getSortKey
    )


if __name__ == "__main__":
    dst_dir = Path().cwd() / 'tlr' / 'char'
    ext = 'main'
    for lang in languages:
        dst_file = dst_dir / f"{lang}.txt"
        try:
            chars = get_exemplars(lang, ext)
            chars.extend(common)

            with open(dst_file, 'w', encoding='utf-8') as f:
                for char in chars:
                    if len(char) != 1 or char.encode('unicode_escape') in blacklist:
                        continue

                    f.write(char + '\n')
        except Exception as e:
            print(f"Error processing language {lang}: {e}")

    dst_file = dst_dir / 'latin.txt'
    all_latin_chars = set()
    for lang in latin_languages:
        src_file = dst_dir / f"{lang}.txt"
        assert src_file.exists(), f"File not found: {src_file}"
        with open(src_file, 'r', encoding='utf-8') as f:
            chars = f.read()
            all_latin_chars.update(set(chars))
    all_latin_chars.discard('\n')
    with open(dst_file, 'w', encoding='utf-8') as f:
        for char in sorted(all_latin_chars):
            f.write(char + '\n')
