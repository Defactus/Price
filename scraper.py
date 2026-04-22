import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import urllib.parse
import re

async def get_mercado_livre_price(page, product_name):
    query = urllib.parse.quote(product_name)
    url = f"https://lista.mercadolivre.com.br/{query}"
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # ML usually has prices in elements with class 'andes-money-amount__fraction'
        # Let's get the first result's price

        # Select the first list item that seems like a product
        product_selector = ".ui-search-result__wrapper"
        await page.wait_for_selector(product_selector, timeout=10000)

        first_product = await page.query_selector(product_selector)
        if first_product:
            price_element = await first_product.query_selector(".andes-money-amount__fraction")
            if price_element:
                price_text = await price_element.inner_text()
                # Clean up the string and convert to float
                price = float(price_text.replace('.', '').replace(',', '.'))
                return price
    except Exception as e:
        print(f"Erro Mercado Livre ({product_name}): {e}")
    return None

async def get_shopee_price(page, product_name):
    query = urllib.parse.quote(product_name)
    url = f"https://shopee.com.br/search?keyword={query}"
    try:
        # Shopee needs more time and usually blocks headless, so we might need to be careful
        await page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for product cards to load
        await page.wait_for_timeout(3000) # Give it a bit extra time to render

        # Find price element
        # Shopee prices are usually like "R$ 10,00"
        price_selector = ".vioxXd.rVLWG6" # Shopee changes these classes frequently, let's try a more generic approach
        # A more generic way: look for elements containing "R$" inside a product card

        # First product card wrapper
        product_card = await page.query_selector("li.col-xs-2-4")
        if not product_card:
            # Fallback selector
            product_card = await page.query_selector(".shopee-search-item-result__item")

        if product_card:
            # Look for price text
            price_elements = await product_card.query_selector_all("span")
            for el in price_elements:
                text = await el.inner_text()
                if "R$" in text:
                    # Extracts number, ignoring 'R$'
                    # Matches something like '1.200,50' or '1200,50'
                    match = re.search(r'R\$\s*([\d\.,]+)', text)
                    if match:
                        price_str = match.group(1).replace('.', '').replace(',', '.')
                        return float(price_str)

            # Another try: Shopee sometimes structures price clearly
            # e.g., <div class="some-class"><span class="currency">R$</span><span class="price">100,00</span></div>
            # Let's try grabbing innerText of the whole card and regex it
            card_text = await product_card.inner_text()
            match = re.search(r'R\$\s*([\d\.,]+)', card_text)
            if match:
                price_str = match.group(1).replace('.', '').replace(',', '.')
                return float(price_str)

    except Exception as e:
        print(f"Erro Shopee ({product_name}): {e}")
    return None

async def main():
    # Read the spreadsheet
    try:
        df = pd.read_excel('produtos.xlsx')
        print("Lendo produtos.xlsx...")
    except Exception as e:
        print(f"Erro ao ler planilha: {e}")
        return

    # Add new columns for the results
    df['Preco_ML'] = None
    df['Preco_Shopee'] = None
    df['Melhor_Preco'] = None
    df['Onde_Comprar'] = None
    df['Abaixo_do_Alvo'] = None

    async with async_playwright() as p:
        # We run non-headless or headless=False might be needed for Shopee to bypass bot detection
        # For a server/Docker, you'd need xvfb or similar. Running headless=True first to see if it works.
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for index, row in df.iterrows():
            produto = row['Produto']
            preco_alvo = row['Preco_Alvo']
            print(f"\nBuscando: {produto} (Alvo: R$ {preco_alvo:.2f})")

            # Scrape Mercado Livre
            preco_ml = await get_mercado_livre_price(page, produto)
            if preco_ml:
                print(f"  Mercado Livre: R$ {preco_ml:.2f}")
                df.at[index, 'Preco_ML'] = preco_ml
            else:
                print("  Mercado Livre: Não encontrado")

            # Scrape Shopee
            preco_shopee = await get_shopee_price(page, produto)
            if preco_shopee:
                print(f"  Shopee: R$ {preco_shopee:.2f}")
                df.at[index, 'Preco_Shopee'] = preco_shopee
            else:
                print("  Shopee: Não encontrado")

            # Comparação
            precos = {}
            if preco_ml: precos['Mercado Livre'] = preco_ml
            if preco_shopee: precos['Shopee'] = preco_shopee

            if precos:
                melhor_loja = min(precos, key=precos.get)
                melhor_preco = precos[melhor_loja]

                df.at[index, 'Melhor_Preco'] = melhor_preco
                df.at[index, 'Onde_Comprar'] = melhor_loja

                if pd.notna(preco_alvo):
                    df.at[index, 'Abaixo_do_Alvo'] = "Sim" if melhor_preco <= preco_alvo else "Não"

            # Pequena pausa para evitar bloqueios
            await asyncio.sleep(2)

        await browser.close()

    # Save results
    output_file = 'resultado_comparacao.xlsx'
    df.to_excel(output_file, index=False)
    print(f"\nBusca finalizada! Resultados salvos em '{output_file}'")

if __name__ == "__main__":
    asyncio.run(main())
