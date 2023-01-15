import sys
import argparse

from src import EpubParser, TextIndex


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
    parser = EpubParser(args.epub_filepath)
    pages = parser.get_pages(args.max_chars_per_page)
    index = TextIndex.build(pages, print=True)
    index.save(args.embeddings_filepath)


if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    create_embeddings(args)
