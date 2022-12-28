import openai


def create_embeddings_for_pages(pages):
    print('Creating embeddings:')
    embeddings = []
    for i in range(len(pages)):
        embedding = create_embedding(pages[i])
        embeddings.append(embedding)
        print('{}/{}'.format(i+1, len(pages)))
    return embeddings


def create_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response['data'][0]['embedding']
    return embedding
