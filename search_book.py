import json
from openai.embeddings_utils import cosine_similarity

from src.create_embeddings import create_embedding

PAGES_FILEPATH = 'pages.json'
QUERY = "the value of water"


def find_best_page(query, pages):
    query_embedding = create_embedding(query)
    best_page = max(pages, key=lambda page: cosine_similarity(query_embedding, json.loads(page['embedding'])))
    return best_page


def read_json(filepath):
    with open(filepath, 'r') as file:
        content = json.load(file)
    return content


if __name__ == '__main__':
    pages = read_json(PAGES_FILEPATH)
    best_page = find_best_page(QUERY, pages)
    print(best_page['text'])
