import requests
import json
import pandas as pd
import urllib.parse

def search_ml(product_name):
    query = urllib.parse.quote(product_name)
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['results'] and len(data['results']) > 0:
            first_result = data['results'][0]
            return first_result['price']
        return None
    except Exception as e:
        print(f"Erro na API ML ({product_name}): {e}")
        return None

df = pd.read_excel('produtos.xlsx')
for index, row in df.iterrows():
    produto = row['Produto']
    print(f"Buscando: {produto}")
    preco = search_ml(produto)
    print(f"Preço: {preco}")
