import ebooklib
import json
from ebooklib import epub
from bs4 import BeautifulSoup


def get_text_from_epub(filepath):
    book = epub.read_epub(filepath, {'ignore_ncx': True})
    # items = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
    items = [book.get_item_with_id('chapter001')]
    text = _get_text_from_items(items)
    return text


def make_pages_from_text(text, page_size):
    paragraphs = text.split('\n')
    paragraphs = filter(None, paragraphs)
    pages = _combine_paragraphs(paragraphs, page_size)
    return pages


def _get_text_from_items(items):
    text_items = map(_get_text_from_item, items)
    return ' '.join(text_items)


def _get_text_from_item(item):
    content = item.get_content()
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    return text


def _combine_paragraphs(paragraphs, page_size):
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
