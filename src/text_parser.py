import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re


class TextParser:
    def __init__(self, text: str):
        self.text = text

    def get_pages(self, max_chars_per_page: int):
        paragraphs = self._get_paragraphs()
        return self._combine_paragraphs(paragraphs, max_chars_per_page)

    def _get_paragraphs(self):
        paragraphs = re.split('\n+', self.text)
        return paragraphs

    def _combine_paragraphs(self, paragraphs, max_chars_per_page):
        pages = []
        current_page = ""
        for paragraph in paragraphs:
            if len(current_page) + len(paragraph) > max_chars_per_page:
                pages.append(current_page.strip())
                current_page = paragraph
            else:
                current_page += '\n' + paragraph
        pages.append(current_page)
        return pages


class EpubParser(TextParser):
    def __init__(self, filepath: str):
        self.text = self._read_file(filepath)
        super().__init__(self.text)

    def _read_file(self, filepath):
        book = epub.read_epub(filepath, {'ignore_ncx': True})
        items = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)
        return self._get_text_from_items(items)

    def _get_text_from_items(self, items):
        text_items = (self._get_text_from_item(item) for item in items)
        return '\n'.join(text_items)

    def _get_text_from_item(self, item):
        content = item.content
        soup = BeautifulSoup(content, 'html.parser')
        return soup.getText()
