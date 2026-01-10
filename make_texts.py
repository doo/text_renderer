import random
import re
import time
from pathlib import Path
from typing import Dict, List

import requests
from tqdm import tqdm

from make_per_language_char_set import currency, language_groups

N_ARTICLES = 300
DELAY_BETWEEN_REQUESTS = 1
DST_DIR = Path().cwd() / 'tlr' / 'text'
DST_DIR.mkdir(parents=True, exist_ok=True)


def make_language_text_file(language: str) -> Path:
    return DST_DIR / f"{language}_text.txt"


def get_wikipedia_articles(
    language: str, n_articles: int = N_ARTICLES
) -> Dict[str, str]:
    articles = {}
    session = requests.Session()
    session.headers.update(
        {'User-Agent': 'TextRenderer/1.0 (https://github.com/oh-my-ocr/text_renderer)'}
    )

    try:
        random_titles_url = (
            f"https://{language}.wikipedia.org/api/rest_v1/page/random/title"
        )
        titles = []

        for _ in tqdm(
            range(n_articles), desc=f"Fetching {language} titles", leave=False
        ):
            try:
                response = session.get(random_titles_url)
                response.raise_for_status()
                data = response.json()
                titles.append(data['items'][0]['title'])
                time.sleep(DELAY_BETWEEN_REQUESTS)
            except Exception as e:
                continue

        titles.sort()

        for title in tqdm(titles, desc=f"Processing {language} articles", leave=False):
            try:
                content_url = f"https://{language}.wikipedia.org/w/api.php"
                params = {
                    'action': 'query',
                    'format': 'json',
                    'titles': title,
                    'prop': 'extracts',
                    'explaintext': True,
                    'exsectionformat': 'plain',
                }
                response = session.get(content_url, params=params)
                response.raise_for_status()
                data = response.json()

                pages = data['query']['pages']
                for _, page_data in pages.items():
                    content = page_data.get('extract', '')
                    if content and content.strip():
                        articles[title] = content

                time.sleep(DELAY_BETWEEN_REQUESTS)

            except requests.RequestException as e:
                continue

    except requests.RequestException as e:
        return {}

    return articles


def save_articles_to_file(language: str, articles: Dict[str, str]) -> None:
    text_file = make_language_text_file(language)

    try:
        with open(text_file, 'w', encoding='utf-8') as f:
            for _, content in articles.items():
                cleaned_content = content.strip()
                if cleaned_content:
                    lines = [
                        line.strip()
                        for line in cleaned_content.split('\n')
                        if line.strip()
                    ]
                    if lines:
                        f.write('\n'.join(lines) + '\n\n')

    except IOError as e:
        print(f"Failed to save articles for language {language}: {e}")


def log_article_titles(language: str, article_titles: List[str]) -> None:
    wiki_dir = Path().cwd() / 'wiki'
    wiki_dir.mkdir(parents=True, exist_ok=True)

    wiki_file = wiki_dir / f"{language}.txt"

    try:
        with open(wiki_file, 'w', encoding='utf-8') as f:
            for title in sorted(article_titles):
                wiki_url = (
                    f"https://{language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
                )
                f.write(wiki_url + '\n')
    except IOError as e:
        print(f"Failed to log article titles for language {language}: {e}")


def process_language(language: str) -> None:
    articles = get_wikipedia_articles(language, N_ARTICLES)
    save_articles_to_file(language, articles)

    article_titles = list(articles.keys())
    log_article_titles(language, article_titles)


def delete_empty_lines_in_file(path: Path) -> None:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(path, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip():
                    f.write(line.strip() + '\n')

    except IOError as e:
        print(f"Failed to delete empty lines in file {path}: {e}")


def delete_sequences_of_whitespaces(path: Path) -> None:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = re.sub(r'\s{2,}', ' ', content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    except IOError as e:
        print(f"Failed to delete sequences of whitespaces in file {path}: {e}")


def add_caps(path: Path) -> None:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(path, 'w', encoding='utf-8') as f:
            for line in lines:
                if random.random() < 0.1:
                    f.write(line.upper())
                elif random.random() < 0.1:
                    words = line.split()
                    modified_words = [
                        word.upper() if random.random() < 0.5 else word
                        for word in words
                    ]
                    f.write(' '.join(modified_words))
                else:
                    f.write(line)

    except IOError as e:
        print(f"Failed to augment texts in file {path}: {e}")


def add_sequences_of_whitespaces(path: Path) -> None:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            if random.random() < 0.1:
                words = line.split()
                if random.random() < 0.5:
                    words = [' ' * random.randint(1, 8)] + words
                if random.random() < 0.5:
                    words = words + [' ' * random.randint(1, 8)]
                separator = ' ' * random.randint(2, 8)

                line = separator.join(words) + '\n'
            f.write(line)


def get_random_float() -> str:
    f = random.uniform(0, 1)
    f *= 10 ** random.randint(0, 5)
    precision = random.randint(0, 3)
    f = round(f, precision)

    if random.random() < 0.5:
        f = int(f)

    cur = random.choice(currency) if random.random() < 0.5 else ''

    if random.random() < 0.5:
        s = cur + str(f)
    else:
        s = str(f) + cur

    return s


def random_remove_whitespace(match):
    return match.group(0).strip() if random.random() < 0.5 else match.group(0)


def add_bullets_and_vertical_lines(path: Path) -> None:
    bullets = '•●*'
    vertical_lines = '|│❘'
    hyphens = '-—−–‒‑־'

    line_starts = bullets + hyphens + '>'
    word_prefixes = '<\'"([{' + bullets + hyphens
    word_suffixes = '>\'")]}…' + bullets + hyphens

    mapping = {
        "RANDOM_FLOAT": get_random_float,
    }
    extra_words = (
        [
            '->',
            '<-',
            '=>',
            '<=',
            '--',
            '---',
            '..',
            '...',
            '***',
            '-->',
            '--->',
            '<--',
            '<---',
            '>>',
            '>>>',
            '<<',
            '<<<',
        ]
        + list(bullets + vertical_lines + hyphens)
        + list(mapping.keys())
    )

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            p = random.random()
            if p < 0.1:
                suffix = (
                    random.choice(line_starts) + ' ' if random.random() < 0.5 else ''
                )
                new_line = f'{suffix}{line}'
            elif p < 0.3:
                words = line.split()
                modified_words = []
                prefix_suffix_flag = random.random() < 0.5
                for word in words:
                    if random.random() < 0.3:
                        extra_word = random.choice(extra_words)
                        if extra_word in mapping:
                            extra_word = mapping[extra_word]()
                        modified_words.append(extra_word)

                    prefix = ''
                    suffix = ''
                    if prefix_suffix_flag:
                        if random.random() < 0.3:
                            prefix = random.choice(word_prefixes)
                        if random.random() < 0.3:
                            suffix = random.choice(word_suffixes)

                    modified_words.append(f"{prefix}{word}{suffix}")
                new_line = ' '.join(modified_words) + '\n'
                new_line = re.sub(r' <|> ', random_remove_whitespace, new_line)
            else:
                new_line = line

            f.write(new_line)


def main() -> None:
    for group, languages in language_groups.items():
        for language in tqdm(languages, desc="Processing languages"):
            process_language(language)
            delete_empty_lines_in_file(make_language_text_file(language))
            delete_sequences_of_whitespaces(make_language_text_file(language))

            if group == 'latin':
                add_caps(make_language_text_file(language))
                add_bullets_and_vertical_lines(make_language_text_file(language))
                add_sequences_of_whitespaces(make_language_text_file(language))


if __name__ == "__main__":
    main()
