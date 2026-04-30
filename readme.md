# Manual do Usuario - Comparador de Precos

Este manual explica como usar o Comparador de Precos para pesquisar produtos em lojas online e gerar uma planilha com os menores e maiores precos encontrados.

O sistema foi feito para usuarios que desejam comparar rapidamente uma lista de produtos a partir de uma planilha Excel.

## 1. O Que o Programa Faz

O Comparador de Precos:

- Le uma planilha `.xlsx` com nomes de produtos.
- Pesquisa os produtos no Mercado Livre.
- Pode tentar pesquisar tambem na Shopee, em modo experimental.
- Gera uma nova planilha com os precos encontrados.
- Informa onde esta o menor preco e se ele esta abaixo do preco alvo definido pelo usuario.

Importante: o programa ajuda na comparacao inicial, mas nao substitui a conferencia manual do anuncio antes da compra.

## 2. Como Baixar e Instalar Sem Git

Voce nao precisa instalar Git para usar este projeto.

Existem tres formas principais de receber ou baixar o programa.

### Opcao A: Receber a Pasta Pronta

Esta e a forma mais simples para usuarios comuns.

Se alguem ja enviou a pasta pronta `PriceComparer`, basta manter a pasta completa no computador e abrir:

```text
PriceComparer.exe
```

Nao copie somente o arquivo `.exe`. Ele precisa ficar junto com a pasta `_internal`.

### Opcao B: Baixar Pelo Navegador

Use esta opcao se voce quer baixar o projeto diretamente do GitHub, sem usar Git.

1. Acesse:

```text
https://github.com/Defactus/Price
```

2. Clique no botao verde `Code`.
3. Clique em `Download ZIP`.
4. Aguarde o download terminar.
5. Clique com o botao direito no arquivo `.zip` baixado.
6. Escolha `Extrair tudo`.
7. Abra a pasta extraida.
8. Se ainda nao existir o executavel, siga a secao `Gerar Um Novo Executavel`.

### Opcao C: Instalacao Quase Automatica Pelo PowerShell

Use esta opcao se voce quer baixar o projeto, preparar o executavel e criar um atalho com poucos comandos.

Antes de executar, instale o Python pelo site oficial:

```text
https://www.python.org/downloads/
```

Durante a instalacao do Python, marque a opcao:

```text
Add python.exe to PATH
```

Depois:

1. Abra o menu Iniciar.
2. Pesquise por `PowerShell`.
3. Abra o `Windows PowerShell`.
4. Cole o comando abaixo e pressione Enter:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; irm https://raw.githubusercontent.com/Defactus/Price/main/instalar_sem_git.ps1 | iex
```

O instalador ira:

- Baixar o projeto do GitHub.
- Extrair os arquivos.
- Instalar as dependencias.
- Baixar o Chromium usado pelo Playwright.
- Gerar o `PriceComparer.exe`.
- Criar um atalho chamado `Comparador de Precos` na Area de Trabalho.

Ao final, o programa ficara instalado em:

```text
C:\Users\SEU_USUARIO\PriceComparer
```

E o executavel ficara em:

```text
C:\Users\SEU_USUARIO\PriceComparer\dist\PriceComparer\PriceComparer.exe
```

Observacao: execute esse comando somente se voce confia na origem do projeto.

### Manual de Comandos Para Baixar e Instalar

Esta opcao mostra todos os comandos usados para baixar e instalar o sistema na maquina, sem precisar de Git.

Abra o `Windows PowerShell` e execute os comandos abaixo.

#### 1. Instalar Python Pelo Terminal

Se o computador ainda nao tiver Python, tente instalar pelo `winget`:

```powershell
winget install Python.Python.3.12
```

Depois feche e abra o PowerShell novamente.

Confira se o Python foi instalado:

```powershell
python --version
```

Se o comando acima nao funcionar, instale manualmente pelo site:

```text
https://www.python.org/downloads/
```

Durante a instalacao manual, marque `Add python.exe to PATH`.

#### 2. Baixar o Projeto Como ZIP

```powershell
$url = "https://github.com/Defactus/Price/archive/refs/heads/main.zip"
$zip = "$env:TEMP\Price-main.zip"
Invoke-WebRequest -Uri $url -OutFile $zip
```

#### 3. Extrair o Projeto

```powershell
$destino = "$env:USERPROFILE\PriceComparer"
$temp = "$env:TEMP\Price-download"
Remove-Item $temp -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive -Path $zip -DestinationPath $temp -Force
Remove-Item $destino -Recurse -Force -ErrorAction SilentlyContinue
Move-Item "$temp\Price-main" $destino
```

#### 4. Entrar na Pasta do Projeto

```powershell
cd "$env:USERPROFILE\PriceComparer"
```

#### 5. Criar Ambiente Python e Instalar Dependencias

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt pyinstaller
```

#### 6. Baixar o Navegador Chromium do Playwright

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH = "0"
.\venv\Scripts\python.exe -m playwright install chromium
```

#### 7. Gerar o Executavel

```powershell
.\venv\Scripts\pyinstaller.exe --noconsole --onedir --name PriceComparer --exclude-module pytest app_gui.py
```

#### 8. Abrir o Programa

```powershell
.\dist\PriceComparer\PriceComparer.exe
```

Depois da instalacao, o programa ficara em:

```text
C:\Users\SEU_USUARIO\PriceComparer\dist\PriceComparer\PriceComparer.exe
```

#### Comando Unico Quase Automatico

Se preferir fazer quase tudo de uma vez, use:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; irm https://raw.githubusercontent.com/Defactus/Price/main/instalar_sem_git.ps1 | iex
```

## 3. Antes de Comecar

Voce precisa ter:

- Um computador com Windows.
- O arquivo executavel do programa.
- Uma planilha Excel no formato `.xlsx`.
- Conexao com a internet.

Se voce recebeu a pasta pronta do sistema, abra o programa pelo arquivo:

```text
C:\DEV\Price\dist\PriceComparer\PriceComparer.exe
```

Nao mova apenas o arquivo `.exe` para outro lugar. Ele depende dos arquivos que ficam dentro da pasta:

```text
C:\DEV\Price\dist\PriceComparer
```

Essa pasta contem componentes internos necessarios para abrir o navegador usado nas buscas.

## 4. Como Preparar a Planilha de Produtos

Crie uma planilha Excel `.xlsx` com pelo menos duas colunas obrigatorias:

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

### Regras da Planilha

- A coluna `Produto` deve conter o nome do item que sera pesquisado.
- A coluna `Preco_Alvo` deve conter o valor maximo desejado para comparacao.
- Os nomes das colunas precisam ser exatamente `Produto` e `Preco_Alvo`.
- A planilha pode ter outras colunas, mas essas duas sao obrigatorias.
- Nao deixe a coluna `Produto` vazia.
- Use numeros simples na coluna `Preco_Alvo`, por exemplo `350`, `199.90` ou `3500`.

Existe um exemplo de planilha em:

```text
C:\DEV\Price\price_scraper\produtos.xlsx
```

## 5. Como Abrir o Programa

1. Abra a pasta:

```text
C:\DEV\Price\dist\PriceComparer
```

2. De dois cliques em:

```text
PriceComparer.exe
```

3. Aguarde a janela do programa abrir.

Se o Windows mostrar um aviso de seguranca, confirme apenas se voce reconhece a origem do arquivo.

## 6. Como Fazer Uma Busca

Na janela do programa:

1. Em `Planilha`, clique em `Selecionar`.
2. Escolha a planilha `.xlsx` com os produtos.
3. Em `Resultado`, confira onde a planilha final sera salva.
4. Se quiser escolher outro local, clique em `Salvar como`.
5. Deixe `Mostrar navegador` marcado se quiser acompanhar a busca na tela.
6. Marque `Tentar Shopee (experimental)` somente se quiser incluir a Shopee.
7. Clique em `Iniciar busca`.
8. Aguarde ate o programa informar que terminou.
9. Clique em `Abrir resultado` ou abra manualmente a planilha gerada.

Durante a busca, o programa mostra mensagens na area de log da janela. Essas mensagens indicam qual produto esta sendo pesquisado e se foram encontrados precos.

## 7. Quando Usar Cada Opcao

### Mostrar navegador

Use esta opcao marcada na maioria dos casos.

Com ela ativada, o navegador usado pelo sistema aparece na tela. Isso ajuda quando algum site pede verificacao, captcha ou carregamento manual.

Se esta opcao for desmarcada, a busca roda em segundo plano. Isso pode ser mais rapido, mas tambem pode aumentar a chance de bloqueios pelos sites.

### Tentar Shopee (experimental)

Use esta opcao apenas quando quiser tentar buscar tambem na Shopee.

A Shopee pode bloquear automacoes, carregar os resultados parcialmente ou pedir captcha. Por isso, essa busca e considerada experimental.

Se a opcao ficar desmarcada, o resultado mostrara `Shopee nao consultado` na coluna `Status`.

## 8. Resultado Gerado

O programa gera uma planilha `.xlsx` com colunas como:

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

### Significado das Principais Colunas

- `Produto`: nome do produto pesquisado.
- `Preco_Alvo`: valor informado na planilha original.
- `Menor_Preco_ML`: menor preco encontrado no Mercado Livre.
- `Maior_Preco_ML`: maior preco encontrado no Mercado Livre.
- `Menor_Preco_Shopee`: menor preco encontrado na Shopee, se consultada.
- `Maior_Preco_Shopee`: maior preco encontrado na Shopee, se consultada.
- `Menor_Preco_Geral`: menor preco encontrado entre todas as lojas consultadas.
- `Onde_Menor_Preco`: loja onde o menor preco foi encontrado.
- `Maior_Preco_Geral`: maior preco encontrado entre todas as lojas consultadas.
- `Onde_Maior_Preco`: loja onde o maior preco foi encontrado.
- `Melhor_Preco`: mesmo valor de `Menor_Preco_Geral`.
- `Onde_Comprar`: loja sugerida com base no menor preco.
- `Abaixo_do_Alvo`: mostra `Sim` quando o menor preco esta abaixo ou igual ao `Preco_Alvo`; caso contrario, mostra `Nao`.
- `Status`: observacoes sobre a busca.

## 9. Possiveis Status

A coluna `Status` pode mostrar:

- `OK`: a busca encontrou precos normalmente.
- `Shopee nao consultado`: a opcao da Shopee nao foi marcada.
- `Mercado Livre nao encontrado`: nao foi possivel encontrar preco no Mercado Livre.
- `Shopee nao encontrado`: nao foi possivel encontrar preco na Shopee.

Mais de uma mensagem pode aparecer no mesmo status, separada por ponto e virgula.

## 10. Como Interpretar os Precos

O sistema coleta varios precos exibidos nos resultados da busca e calcula o menor e o maior valor encontrado.

Por isso, confira sempre o anuncio antes de comprar. O menor ou maior preco pode representar:

- Produto parecido, mas nao exatamente igual.
- Acessorio em vez do produto principal.
- Produto usado.
- Variacao de cor, memoria, tamanho ou modelo.
- Kit com mais itens.
- Anuncio patrocinado.
- Promocao temporaria.

O programa nao compara:

- Frete.
- Prazo de entrega.
- Reputacao do vendedor.
- Estoque.
- Cupons.
- Parcelamento.
- Garantia.
- Condicao do produto.

## 11. Problemas Comuns e Como Resolver

### A planilha nao abre ou da erro

Verifique se:

- O arquivo esta no formato `.xlsx`.
- As colunas `Produto` e `Preco_Alvo` existem.
- Os nomes das colunas estao escritos exatamente dessa forma.
- Existe pelo menos um produto preenchido.
- A planilha nao esta aberta e bloqueada pelo Excel.

### O programa nao encontrou precos

Possiveis causas:

- O site mudou o layout.
- O produto foi digitado de forma muito generica ou muito especifica.
- O site bloqueou a automacao.
- A internet esta instavel.
- O resultado exigiu captcha.

Tente:

- Usar nomes de produtos mais claros.
- Marcar `Mostrar navegador`.
- Rodar novamente depois de alguns minutos.
- Conferir manualmente se o produto aparece no site.

### Apareceu captcha

Se o navegador estiver visivel, resolva o captcha manualmente e aguarde o programa continuar.

Se o navegador nao estiver visivel, rode novamente com `Mostrar navegador` marcado.

### O executavel nao abre

Verifique se:

- Voce esta abrindo o arquivo dentro da pasta `dist\PriceComparer`.
- A pasta `_internal` ainda existe.
- O antivirus nao removeu algum arquivo do programa.
- Voce tem permissao para executar programas nessa pasta.

## 12. Limitacoes Conhecidas

Este tipo de automacao depende dos sites pesquisados.

Limitacoes atuais:

- O Mercado Livre pode mudar a pagina e exigir ajuste no sistema.
- A Shopee pode bloquear a busca com mais frequencia.
- Captchas precisam ser resolvidos manualmente.
- O pacote final e grande porque inclui o navegador Chromium.
- Os precos coletados devem ser tratados como referencia inicial, nao como garantia de compra.

## 13. Uso Avancado Pela Linha de Comando

Esta secao e destinada a usuarios tecnicos.

### Requisitos

- Python 3.8 ou superior.
- Dependencias do arquivo `requirements.txt`.
- Chromium instalado pelo Playwright.

### Instalacao

Execute na pasta do projeto:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m playwright install chromium
```

### Abrir a Interface Grafica Pelo Codigo

```powershell
.\venv\Scripts\python.exe app_gui.py
```

### Rodar Pela Linha de Comando

```powershell
.\venv\Scripts\python.exe app_cli.py produtos.xlsx
```

Para mostrar o navegador durante a busca:

```powershell
.\venv\Scripts\python.exe app_cli.py produtos.xlsx --show-browser
```

Para escolher o arquivo de saida:

```powershell
.\venv\Scripts\python.exe app_cli.py produtos.xlsx --output resultado_comparacao.xlsx
```

Para tentar incluir a Shopee:

```powershell
.\venv\Scripts\python.exe app_cli.py produtos.xlsx --show-browser --include-shopee
```

## 14. Gerar Um Novo Executavel

Esta secao e destinada a manutencao do sistema.

Execute na pasta do projeto:

```powershell
.\build_exe.ps1
```

O executavel sera criado em:

```text
dist\PriceComparer\PriceComparer.exe
```

O build usa PyInstaller no formato `onedir`, porque o Playwright precisa incluir arquivos do Chromium junto com o aplicativo.

## 15. Rodar Testes

Instale as dependencias de desenvolvimento:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Rode os testes:

```powershell
.\venv\Scripts\python.exe -m pytest tests
```

## 16. Boas Praticas de Uso

- Pesquise poucos produtos no primeiro teste.
- Use nomes de produtos claros e completos.
- Confira o arquivo de resultado antes de tomar decisoes de compra.
- Salve uma copia da planilha original antes de fazer alteracoes.
- Rode novamente a busca se algum site carregar de forma incompleta.
- Mantenha a pasta do programa completa ao mover para outro computador.
