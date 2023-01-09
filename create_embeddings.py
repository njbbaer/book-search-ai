import json
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse

from src.util import create_embedding


def read_epub_text(filepath):
    book = epub.read_epub(filepath, {'ignore_ncx': True})
    items = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    text = get_text_from_items(items)
    return text


def make_pages_from_text(text, page_size):
    paragraphs = text.split('\n')
    paragraphs = filter(None, paragraphs)
    pages = combine_paragraphs(paragraphs, page_size)
    return pages


def get_text_from_items(items):
    text_items = map(get_text_from_item, items)
    return ' '.join(text_items)


def get_text_from_item(item):
    content = item.get_content()
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    return text


def combine_paragraphs(paragraphs, max_chars_per_page):
    pages = []
    current_page = ""
    for paragraph in paragraphs:
        if len(current_page) + len(paragraph) > max_chars_per_page:
            pages.append(current_page.strip())
            current_page = paragraph
        else:
            current_page += ' ' + paragraph
    pages.append(current_page)
    return pages


def create_embeddings_for_pages(pages):
    embeddings = []
    for i in tqdm(range(len(pages))):
        embedding = create_embedding(pages[i])
        embeddings.append(embedding)
    return embeddings


def format_pages_with_embeddings(pages, embeddings):
    pages_with_embeddings = []
    for i in range(len(pages)):
        pages_with_embeddings.append({
            'id': i,
            'text': pages[i],
            'embedding': str(embeddings[i])
        })
    return pages_with_embeddings


def write_embeddings_json(content, filepath):
    with open(filepath, 'w') as file:
        json.dump(content, file, indent=2, ensure_ascii=False)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('epub_filepath',
                        help='filepath of the EPUB file')
    parser.add_argument('-c', '--max_chars_per_page', type=int, default=1000,
                        help='number of characters per page')
    parser.add_argument('-e', '--embeddings_filepath', default='embeddings.json',
                        help='filepath to write the page embeddings')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    text = read_epub_text(args.epub_filepath)
    pages = make_pages_from_text(text, args.max_chars_per_page)
    cost = len(text) / 4 / 1000 * 0.0004
    print('Embedding {} characters, as {} pages, for ~${:0.2f}.'.format(len(text), len(pages), cost))
    embeddings = create_embeddings_for_pages(pages)
    pages_with_embeddings = format_pages_with_embeddings(pages, embeddings)
    write_embeddings_json(pages_with_embeddings, args.embeddings_filepath)
