import time
from pathlib import Path
from typing import Dict, List

import requests
from tqdm import tqdm

from make_per_language_char_set import languages

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


def main() -> None:
    for language in tqdm(languages, desc="Processing languages"):
        process_language(language)
        delete_empty_lines_in_file(make_language_text_file(language))


if __name__ == "__main__":
    main()
