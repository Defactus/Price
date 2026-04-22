import asyncio
from playwright.async_api import async_playwright
import pandas as pd
import urllib.parse
import re
import os

async def get_mercado_livre_price(page, product_name):
    query = urllib.parse.quote(product_name.replace(" ", "-"))
    url = f"https://lista.mercadolivre.com.br/{query}"
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(2000)

        price_fraction = await page.query_selector('.andes-money-amount__fraction')
        if price_fraction:
            price_text = await price_fraction.inner_text()
            return float(price_text.replace('.', '').replace(',', '.'))

        return None
    except Exception as e:
        print(f"Erro Mercado Livre: {e}")
        return None

async def get_shopee_price(page, product_name):
    query = urllib.parse.quote(product_name)
    url = f"https://shopee.com.br/search?keyword={query}"
    try:
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(5000)

        content = await page.inner_text("body")
        match = re.search(r'R\$\s*([\d\.,]+)', content)
        if match:
             price_str = match.group(1).replace('.', '').replace(',', '.')
             return float(price_str)

        return None
    except Exception as e:
        print(f"Erro Shopee: {e}")
        return None

async def run_scraper(input_file, update_status_callback):
    update_status_callback(f"Lendo arquivo: {os.path.basename(input_file)}", 5)

    try:
        df = pd.read_excel(input_file)
    except Exception as e:
        raise Exception(f"Não foi possível ler o arquivo Excel: {e}")

    df['Preco_ML'] = None
    df['Preco_Shopee'] = None
    df['Melhor_Preco'] = None
    df['Onde_Comprar'] = None
    df['Abaixo_do_Alvo'] = None

    total_items = len(df)

    async with async_playwright() as p:
        update_status_callback("Abrindo navegador...", 10)
        browser = await p.chromium.launch(
            headless=False, # Must be visible for anti-bot
            args=['--disable-blink-features=AutomationControlled']
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1366, 'height': 768}
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = await context.new_page()

        for index, row in df.iterrows():
            produto = row['Produto']
            preco_alvo = row.get('Preco_Alvo', None)

            base_progress = 10 + (index / total_items * 80)
            update_status_callback(f"Buscando ({index+1}/{total_items}): {produto}", base_progress)

            preco_ml = await get_mercado_livre_price(page, produto)
            if preco_ml:
                df.at[index, 'Preco_ML'] = preco_ml

            preco_shopee = await get_shopee_price(page, produto)
            if preco_shopee:
                df.at[index, 'Preco_Shopee'] = preco_shopee

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

        update_status_callback("Fechando navegador e salvando resultados...", 95)
        await browser.close()

    output_file = os.path.join(os.path.dirname(input_file), 'resultado_comparacao.xlsx')
    df.to_excel(output_file, index=False)
    update_status_callback(f"Salvo em: {os.path.basename(output_file)}", 100)
