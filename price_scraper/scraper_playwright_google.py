import asyncio
from playwright.async_api import async_playwright
import urllib.parse
import re
import pandas as pd

async def search_price_google(page, product_name, store_domain):
    query = urllib.parse.quote(f"site:{store_domain} {product_name} preço")
    url = f"https://www.google.com/search?q={query}"

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Wait for some results to appear
        await page.wait_for_timeout(2000)

        # Extract all text and look for R$
        content = await page.inner_text("body")

        # This regex looks for R$ followed by numbers
        prices = re.findall(r'R\$\s*([\d\.,]+)', content)

        if prices:
            # Filter and convert prices
            valid_prices = []
            for p in prices:
                # Remove dots, replace comma with dot
                try:
                    p_val = float(p.replace('.', '').replace(',', '.'))
                    # Ignore weirdly low prices that might be installments
                    if p_val > 10:
                        valid_prices.append(p_val)
                except:
                    pass

            if valid_prices:
                # Often Google shows the price in the snippet, we just return the most reasonable one or first one
                # Usually we want to return the lowest reasonable price or just the first one found
                # For simplicity, returning the lowest
                return min(valid_prices)

        return None

    except Exception as e:
        print(f"Erro no Google ({store_domain}): {e}")
        return None

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='pt-BR'
        )
        page = await context.new_page()

        produto = "Smartphone Samsung Galaxy S23"

        print(f"Buscando via Google: {produto}")

        preco_ml = await search_price_google(page, produto, "mercadolivre.com.br")
        print(f"Mercado Livre (via Google): R$ {preco_ml}")

        preco_shopee = await search_price_google(page, produto, "shopee.com.br")
        print(f"Shopee (via Google): R$ {preco_shopee}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
