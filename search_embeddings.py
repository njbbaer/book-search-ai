import json
import argparse
from openai.embeddings_utils import cosine_similarity

from src.util import create_embedding


def read_json(filepath):
    with open(filepath, 'r') as file:
        content = json.load(file)
    return content


def find_best_page(search_text, pages):
    search_embedding = create_embedding(search_text)
    best_page = max(pages, key=lambda page: cosine_similarity(search_embedding, json.loads(page['embedding'])))
    return best_page


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('search_text', help='text to search for')
    parser.add_argument('-e', '--embeddings_filepath', default='embeddings.json',
                        help='filepath of the page embeddings')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_arguments()
    pages = read_json(args.embeddings_filepath)
    best_page = find_best_page(args.search_text, pages)
    print(best_page['text'])
