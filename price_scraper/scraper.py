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

        product_selector = ".ui-search-result__wrapper"
        await page.wait_for_selector(product_selector, timeout=10000)

        first_product = await page.query_selector(product_selector)
        if first_product:
            price_element = await first_product.query_selector(".andes-money-amount__fraction")
            if price_element:
                price_text = await price_element.inner_text()
                price = float(price_text.replace('.', '').replace(',', '.'))
                return price
    except Exception as e:
        print(f"Erro Mercado Livre ({product_name}): {e}")
    return None

async def get_shopee_price(page, product_name):
    query = urllib.parse.quote(product_name)
    url = f"https://shopee.com.br/search?keyword={query}"
    try:
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)

        product_card = await page.query_selector("li.col-xs-2-4")
        if not product_card:
            product_card = await page.query_selector(".shopee-search-item-result__item")

        if product_card:
            card_text = await product_card.inner_text()
            match = re.search(r'R\$\s*([\d\.,]+)', card_text)
            if match:
                price_str = match.group(1).replace('.', '').replace(',', '.')
                return float(price_str)

    except Exception as e:
        print(f"Erro Shopee ({product_name}): {e}")
    return None

async def main():
    try:
        df = pd.read_excel('produtos.xlsx')
        print("Lendo produtos.xlsx...")
    except Exception as e:
        print(f"Erro ao ler planilha: {e}")
        return

    df['Preco_ML'] = None
    df['Preco_Shopee'] = None
    df['Melhor_Preco'] = None
    df['Onde_Comprar'] = None
    df['Abaixo_do_Alvo'] = None

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for index, row in df.iterrows():
            produto = row['Produto']
            preco_alvo = row['Preco_Alvo']
            print(f"\nBuscando: {produto} (Alvo: R$ {preco_alvo:.2f})")

            preco_ml = await get_mercado_livre_price(page, produto)
            if preco_ml:
                print(f"  Mercado Livre: R$ {preco_ml:.2f}")
                df.at[index, 'Preco_ML'] = preco_ml
            else:
                print("  Mercado Livre: Não encontrado")

            preco_shopee = await get_shopee_price(page, produto)
            if preco_shopee:
                print(f"  Shopee: R$ {preco_shopee:.2f}")
                df.at[index, 'Preco_Shopee'] = preco_shopee
            else:
                print("  Shopee: Não encontrado")

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

            await asyncio.sleep(2)

        await browser.close()

    output_file = 'resultado_comparacao.xlsx'
    df.to_excel(output_file, index=False)
    print(f"\nBusca finalizada! Resultados salvos em '{output_file}'")

if __name__ == "__main__":
    asyncio.run(main())
