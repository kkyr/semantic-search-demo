import chromadb
import openai


class Collection:
    def __init__(self, openai_api_key):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(name="products", get_or_create=True)
        openai.api_key = openai_api_key

    def add(self, products):
        embeddings = [Collection.__get_embedding(p['description']) for p in products]
        ids = [str(p['id']) for p in products]
        documents = [p['description'] for p in products]
        metadata = [{'brand': p['brand'], 'price': p['price']} for p in products]
        self.collection.add(ids=ids, documents=documents, metadatas=metadata, embeddings=embeddings)

    def get(self, query, n_results=2, brand=None):
        embedding = Collection.__get_embedding(query)
        where = {'brand': brand} if brand else {}
        result = self.collection.query(query_embeddings=[embedding], n_results=n_results, where=where)
        return Collection.__convert_to_products(result)

    @staticmethod
    def __get_embedding(text, model="text-embedding-ada-002"):
        return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

    @staticmethod
    def __convert_to_products(result):
        num_products = len(result['ids'][0])
        products = [
            {
                'id': result['ids'][0][i],
                'description': result['documents'][0][i],
                'brand': result['metadatas'][0][i]['brand'],
                'price': result['metadatas'][0][i]['price'],
                'distance': result['distances'][0][i]
            } for i in range(num_products)
        ]
        return products
