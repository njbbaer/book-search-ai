import ebooklib
import json
from ebooklib import epub
from bs4 import BeautifulSoup


def get_text_from_epub(file_path):
    book = epub.read_epub(file_path, {'ignore_ncx': True})
    items = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    text = get_text_from_items(items)
    return text


def get_text_from_items(items):
    text_items = map(get_text_from_item, items)
    return ' '.join(text_items)


def get_text_from_item(item):
    content = item.get_content()
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    return text


def make_pages_from_text(text, page_size):
    paragraphs = text.split('\n')
    paragraphs = filter(None, paragraphs)
    pages = combine_paragraphs(paragraphs, page_size)
    return pages


def combine_paragraphs(paragraphs, page_size):
    pages = []
    current_page = ""
    for paragraph in paragraphs:
        if len(current_page) + len(paragraph) > page_size:
            pages.append(current_page.strip())
            current_page = paragraph
        else:
            current_page += ' ' + paragraph
    pages.append(current_page)
    return pages


def write_pages_to_json(pages, filepath):
    content = []
    for i in range(len(pages)):
        content.append({'id': i, 'text': pages[i]})
    with open(filepath, 'w') as file:
        json.dump(content, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    text = get_text_from_epub('dune.epub')
    pages = make_pages_from_text(text, 1000)
    write_pages_to_json(pages, 'dune.json')
