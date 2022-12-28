import json

from src.parse_epub import get_text_from_epub, make_pages_from_text
from src.create_embeddings import create_embeddings_for_pages

EPUB_FILEPATH = 'dune.epub'
PAGES_FILEPATH = 'pages.json'
CHARS_PER_PAGE = 1000


def write_to_json(content, filepath):
    with open(filepath, 'w') as file:
        json.dump(content, file, indent=2, ensure_ascii=False)


def format_pages_with_embeddings(pages, embeddings):
    pages_with_embeddings = []
    for i in range(len(pages)):
        pages_with_embeddings.append({
            'id': i,
            'text': pages[i],
            'embedding': str(embeddings[i])
        })
    return pages_with_embeddings


if __name__ == '__main__':
    text = get_text_from_epub(EPUB_FILEPATH)
    pages = make_pages_from_text(text, CHARS_PER_PAGE)
    print('Made {} pages, from {} characters.'.format(len(pages), len(text)))
    embeddings = create_embeddings_for_pages(pages)
    pages_with_embeddings = format_pages_with_embeddings(pages, embeddings)
    write_to_json(pages_with_embeddings, PAGES_FILEPATH)
    print('Done.')
