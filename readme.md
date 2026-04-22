# Scraper de Preços (Mercado Livre & Shopee)

Este robô lê uma planilha Excel (`produtos.xlsx`) com uma lista de produtos, busca os preços no Mercado Livre e na Shopee e gera um novo arquivo (`resultado_comparacao.xlsx`) informando qual o melhor preço e onde comprar.

## Requisitos

- Python 3.8+
- Bibliotecas necessárias listadas em `requirements.txt`

## Instalação

Abra o terminal na pasta do projeto e instale as dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Configuração

1. Crie ou atualize o arquivo `produtos.xlsx` na mesma pasta do script.
2. O arquivo deve conter pelo menos as seguintes colunas:
   - `Produto`: O nome do produto que deseja pesquisar.
   - `Preco_Alvo`: O preço que você considera o ideal (para fins de comparação).

## Execução

Devido aos sistemas avançados anti-bot (captchas) que Mercado Livre e Shopee implementam, rodar scripts de automação em servidores Cloud com navegadores em modo invisível (headless) costuma resultar em bloqueios imediatos, a menos que se usem proxies residenciais caros.

**Para operar com Custo Zero, você deve rodar este script LOCALMENTE na sua máquina.**

O script principal `scraper_local.py` foi projetado para rodar com a interface gráfica do navegador ativada (`headless=False`). Isso ajuda a reduzir as chances de bloqueio pelas lojas e, caso apareça um Captcha, você pode resolvê-lo manualmente para que o script continue.

Execute o código com:

```bash
python3 scraper_local.py
```
