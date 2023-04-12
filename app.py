import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from products import Collection

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

collection = Collection(openai_api_key)

with open('products.json', 'r') as f:
    products = json.load(f)
    collection.add(products)

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('public', 'index.html')


@app.route('/products', methods=['GET'])
def products():
    try:
        query = request.args.get('query')
        if not query:
            return {}
        brand = request.args.get('brand')
        results = collection.get(query=query, brand=brand, n_results=3)
        return jsonify({'products': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
