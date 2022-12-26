import json
import openai


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


def write_pages(pages, filepath):
    with open(filepath, 'w') as file:
        json.dump(pages, file, indent=2, ensure_ascii=False)


def add_embeddings(pages):
    pages = pages.copy()
    for i in range(len(pages)):
        text = pages[i]['text']
        pages[i]['embedding'] = str(create_embedding(text))
        print('Page {}/{} done.'.format(i+1, len(pages)))
    return pages


if __name__ == '__main__':
    pages = read_pages('pages.json')
    pages_with_embeddings = add_embeddings(pages)
    write_pages(pages_with_embeddings, 'pages.json')
