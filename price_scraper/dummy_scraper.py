import pandas as pd
import random
import time

def scrape_prices():
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

    print("\nIniciando raspagem de preços (Simulada)...")

    for index, row in df.iterrows():
        produto = row['Produto']
        preco_alvo = row['Preco_Alvo']

        print(f"\nBuscando: {produto}")
        time.sleep(1) # Simulating network request

        # Simulating scraped prices around the target price
        if pd.notna(preco_alvo):
            preco_ml = round(preco_alvo * random.uniform(0.9, 1.2), 2)
            preco_shopee = round(preco_alvo * random.uniform(0.85, 1.15), 2)
        else:
            preco_ml = round(random.uniform(100, 5000), 2)
            preco_shopee = round(random.uniform(100, 5000), 2)

        print(f"  Encontrado no Mercado Livre: R$ {preco_ml}")
        print(f"  Encontrado na Shopee: R$ {preco_shopee}")

        df.at[index, 'Preco_ML'] = preco_ml
        df.at[index, 'Preco_Shopee'] = preco_shopee

        precos = {'Mercado Livre': preco_ml, 'Shopee': preco_shopee}
        melhor_loja = min(precos, key=precos.get)
        melhor_preco = precos[melhor_loja]

        df.at[index, 'Melhor_Preco'] = melhor_preco
        df.at[index, 'Onde_Comprar'] = melhor_loja

        if pd.notna(preco_alvo):
            df.at[index, 'Abaixo_do_Alvo'] = "Sim" if melhor_preco <= preco_alvo else "Não"

    output_file = 'resultado_comparacao.xlsx'
    df.to_excel(output_file, index=False)
    print(f"\nBusca finalizada! Resultados salvos em '{output_file}'")

if __name__ == "__main__":
    scrape_prices()
