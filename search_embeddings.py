import json
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity


def create_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response['data'][0]['embedding']
    return embedding


def read_pages(filepath):
    with open(filepath) as file:
        pages = json.load(file)
    return pages


def find_best_page(query, pages):
    query_embedding = create_embedding(query)
    best_page = max(pages, key=lambda page: cosine_similarity(query_embedding, json.loads(page['embedding'])))
    return best_page


if __name__ == '__main__':
    pages = read_pages('pages.json')
    query = "search query goes here"
    best_page = find_best_page(query, pages)
    print(best_page['text'])
