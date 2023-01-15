import argparse

from text_index import TextIndex


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_text', help='text to search for')
    parser.add_argument('-e', '--embeddings_filepath', default='embeddings.json',
                        help='filepath of the page embeddings')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    index = TextIndex.load(args.embeddings_filepath)
    print(index.search(args.search_text))
