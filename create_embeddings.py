import json
import ebooklib
import sys
import argparse
from ebooklib import epub
from bs4 import BeautifulSoup
from tqdm import tqdm

from text_parser import EpubParser
from src.util import create_embedding


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


def print_stats(pages):
    text = ''.join(pages)
    num_chars = len(text)
    num_pages = len(pages)
    cost = num_chars / 4 / 1000 * 0.0004
    print('Embedding {} characters, as {} pages, for ~${:0.2f}.'.format(num_chars, num_pages, cost))


def parse_arguments(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('epub_filepath',
                        help='filepath of the EPUB file')
    parser.add_argument('-c', '--max_chars_per_page', type=int, default=1000,
                        help='number of characters per page')
    parser.add_argument('-e', '--embeddings_filepath', default='embeddings.json',
                        help='filepath to write the page embeddings')
    args = parser.parse_args(args)
    return args


def create_embeddings(args):
    epub_parser = EpubParser(args.epub_filepath)
    pages = epub_parser.get_pages(args.max_chars_per_page)
    print_stats(pages)
    embeddings = create_embeddings_for_pages(pages)
    pages_with_embeddings = format_pages_with_embeddings(pages, embeddings)
    write_embeddings_json(pages_with_embeddings, args.embeddings_filepath)

if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    create_embeddings(args)
