# Manual de Uso - Comparador de Precos

Este aplicativo compara precos de produtos usando uma planilha Excel como entrada.

Ele consulta o Mercado Livre como fonte principal, pode tentar consultar a Shopee em modo experimental, e gera uma nova planilha com menor preco, maior preco, melhor loja e status da busca.

## 1. Onde Abrir o Programa

Abra o executavel:

```text
C:\DEV\Price\dist\PriceComparer\PriceComparer.exe
```

Importante: mantenha a pasta inteira `dist\PriceComparer`. O arquivo `.exe` depende da pasta `_internal`, que contem o navegador Chromium usado pelo sistema.

## 2. Como Preparar a Planilha

Crie uma planilha Excel `.xlsx` com pelo menos duas colunas:

```text
Produto
Preco_Alvo
```

Exemplo:

| Produto | Preco_Alvo |
| --- | ---: |
| Controle PS5 DualSense | 350 |
| Smartphone Samsung Galaxy S23 | 3500 |
| Monitor Dell 24 | 800 |

Regras:

- `Produto`: nome que sera pesquisado nos sites.
- `Preco_Alvo`: valor usado para dizer se o menor preco encontrado esta abaixo do alvo.
- O nome das colunas precisa ser exatamente `Produto` e `Preco_Alvo`.
- A planilha pode ter outras colunas, mas essas duas sao obrigatorias.
- Existe um exemplo em `price_scraper\produtos.xlsx`.

## 3. Como Rodar a Busca

1. Abra o `PriceComparer.exe`.
2. No campo `Planilha`, clique em `Selecionar`.
3. Escolha sua planilha `.xlsx`.
4. No campo `Resultado`, confira onde o arquivo final sera salvo.
5. Mantenha `Mostrar navegador` marcado se quiser acompanhar a busca.
6. Marque `Tentar Shopee (experimental)` somente se quiser incluir a Shopee.
7. Clique em `Iniciar busca`.
8. Aguarde a conclusao.
9. Abra o arquivo de resultado gerado.

## 4. Resultado Gerado

O aplicativo gera uma planilha `.xlsx` com as principais colunas:

```text
Produto
Preco_Alvo
Menor_Preco_ML
Maior_Preco_ML
Menor_Preco_Shopee
Maior_Preco_Shopee
Menor_Preco_Geral
Onde_Menor_Preco
Maior_Preco_Geral
Onde_Maior_Preco
Melhor_Preco
Onde_Comprar
Abaixo_do_Alvo
Status
```

Significado das colunas:

- `Menor_Preco_ML`: menor preco encontrado no Mercado Livre.
- `Maior_Preco_ML`: maior preco encontrado no Mercado Livre.
- `Menor_Preco_Shopee`: menor preco encontrado na Shopee, se a opcao estiver ativa.
- `Maior_Preco_Shopee`: maior preco encontrado na Shopee, se a opcao estiver ativa.
- `Menor_Preco_Geral`: menor preco encontrado entre as lojas consultadas.
- `Onde_Menor_Preco`: loja onde o menor preco foi encontrado.
- `Maior_Preco_Geral`: maior preco encontrado entre as lojas consultadas.
- `Onde_Maior_Preco`: loja onde o maior preco foi encontrado.
- `Melhor_Preco`: igual ao menor preco geral.
- `Onde_Comprar`: loja sugerida com base no menor preco.
- `Abaixo_do_Alvo`: `Sim` se o menor preco geral for menor ou igual ao `Preco_Alvo`; caso contrario, `Nao`.
- `Status`: observacoes sobre a busca.

Possiveis valores de `Status`:

- `OK`
- `Shopee nao consultado`
- `Mercado Livre nao encontrado`
- `Shopee nao encontrado`

## 5. Observacoes Sobre Menor e Maior Preco

O sistema coleta varios precos exibidos nos resultados da busca e calcula o menor e o maior.

Isso significa que:

- O menor preco pode ser de uma promocao, variacao, produto usado, acessorio ou anuncio parecido.
- O maior preco pode ser de kit, variacao premium, produto patrocinado ou anuncio diferente.
- A comparacao ajuda na triagem, mas o usuario deve conferir o anuncio antes de comprar.
- O aplicativo nao compara frete, prazo, reputacao, estoque, cupons ou parcelamento.

## 6. Limitacoes Conhecidas

Este tipo de automacao depende dos sites consultados.

Limites conhecidos:

- Mercado Livre pode mudar o layout e exigir ajuste no extrator.
- Shopee costuma bloquear automacao, carregar parcialmente ou exigir captcha.
- O primeiro, menor ou maior resultado pode nao ser exatamente o produto desejado.
- Captchas precisam ser resolvidos manualmente quando aparecerem.
- O pacote final e grande porque inclui o Chromium usado pelo Playwright.

## 7. Rodar Pelo Codigo

Requisitos:

- Python 3.8+
- Dependencias de `requirements.txt`
- Chromium do Playwright

Instalacao:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m playwright install chromium
```

Abrir interface:

```powershell
.\venv\Scripts\python.exe app_gui.py
```

Rodar por linha de comando:

```powershell
.\venv\Scripts\python.exe app_cli.py produtos.xlsx --show-browser
```

Tentar incluir Shopee:

```powershell
.\venv\Scripts\python.exe app_cli.py produtos.xlsx --show-browser --include-shopee
```

## 8. Gerar Novo EXE

Execute na pasta do projeto:

```powershell
.\build_exe.ps1
```

O executavel sera gerado em:

```text
dist\PriceComparer\PriceComparer.exe
```

O build usa PyInstaller em modo `onedir`, porque o Playwright precisa levar arquivos do Chromium junto com o aplicativo.

## 9. Testes

Instalar dependencias de desenvolvimento:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Rodar testes:

```powershell
.\venv\Scripts\python.exe -m pytest tests
```
