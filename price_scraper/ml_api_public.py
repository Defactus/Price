import requests
import json
import urllib.parse

def search_ml_public(product_name):
    query = urllib.parse.quote(product_name)
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}&limit=1"

    headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                first_result = data['results'][0]
                return first_result['price']
        else:
            print(f"Erro {response.status_code}: {response.text[:100]}")
    except Exception as e:
        print(f"Exception: {e}")
    return None

print(f"ML API Public Price: {search_ml_public('Smartphone Samsung Galaxy S23')}")
