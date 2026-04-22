import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
import re

def get_mercado_livre_price(product_name):
    query = urllib.parse.quote(product_name)
    url = f"https://lista.mercadolivre.com.br/{query}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # The structure might have changed. Let's try some common ones
            # 1. Newest structure
            price_fraction = soup.find('span', class_='andes-money-amount__fraction')

            if price_fraction:
                price_text = price_fraction.text.strip()
                price = float(price_text.replace('.', '').replace(',', '.'))
                return price

            # Let's see if we hit a captcha by checking title
            if "Mercado Livre" in soup.title.text and "Bot" in soup.title.text:
                print(f"ML bloqueou a requisição (Captcha)")
                return None

        else:
            print(f"Erro ML HTTP {response.status_code}")
    except Exception as e:
        print(f"Erro ML: {e}")

    return None

print(f"Teste ML com BeautifulSoup: {get_mercado_livre_price('Smartphone Samsung Galaxy S23')}")
