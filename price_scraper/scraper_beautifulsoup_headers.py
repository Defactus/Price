import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def get_ml_price(product_name):
    query = urllib.parse.quote(product_name.replace(' ', '-'))
    url = f"https://lista.mercadolivre.com.br/{query}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        response = requests.get(url, headers=headers)
        print(f"Status ML: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # ML changes its structure often. Let's try to extract any price using regex if specific classes fail
        # Usually it's in <span class="andes-money-amount__fraction">
        price_tags = soup.find_all('span', class_='andes-money-amount__fraction')
        if price_tags:
            return float(price_tags[0].text.replace('.', '').replace(',', '.'))

        print("Price tag not found.")
        # Check for captcha or blocks
        title = soup.title.string if soup.title else 'No title'
        print(f"Page title: {title}")

    except Exception as e:
        print(f"Error: {e}")

    return None

def get_shopee_price(product_name):
    query = urllib.parse.quote(product_name)
    url = f"https://shopee.com.br/search?keyword={query}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers)
        print(f"Status Shopee: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        # Shopee is heavily client-side rendered, so Beautiful Soup is likely not going to find prices.
        # But we can try to look at the script tags for JSON data
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and 'price' in script.string:
                # Might be able to regex out a price
                pass

        print("Shopee is mostly JS rendered, might not work well with BS4.")
    except Exception as e:
         print(f"Error: {e}")

    return None

print(f"ML: {get_ml_price('smartphone samsung galaxy s23')}")
print(f"Shopee: {get_shopee_price('smartphone samsung galaxy s23')}")
