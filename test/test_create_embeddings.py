import unittest
import requests_mock
from create_embeddings import create_embeddings, parse_arguments


class TestCreateEmbeddings(unittest.TestCase):
    def test_create_embeddings(self):
        with requests_mock.Mocker() as m:
            response_body = {
                'data': [
                    {
                        'embedding': [0.1, 0.2, 0.3]
                    }
                ]
            }
            m.post('https://api.openai.com/v1/embeddings', json=response_body)
            args = parse_arguments(['test/fixtures/example_book.epub'])
            create_embeddings(args)
