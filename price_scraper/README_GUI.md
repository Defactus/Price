# Bot de Preços com Interface Gráfica

Esta versão contém uma interface gráfica leve e pode ser compilada para Windows como um arquivo executável (`.exe`).

## Rodando via Python

1. Crie o ambiente virtual e instale dependências:
```bash
python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
playwright install chromium
```

2. Execute o aplicativo:
```bash
python3 app_gui.py
```
*(Uma janela abrirá para você selecionar a planilha `produtos.xlsx` e iniciar o bot).*

## Gerando o `.exe` no Windows

Para gerar o arquivo executável que funciona em computadores sem Python:

1. Certifique-se de estar usando Windows com Python instalado.
2. Dê um duplo-clique no arquivo `setup_windows.bat`.
3. Aguarde o processo finalizar.
4. O seu bot estará na pasta `dist\Bot_Precos`. Você pode copiar esta pasta para onde quiser ou compactá-la para enviar a outras pessoas. O arquivo a ser aberto é o `Bot_Precos.exe`.

> **Aviso de Anti-Bot**: Como a automação de navegadores exige passar por bloqueios, o navegador Chromium será aberto de forma visível na tela durante a extração dos dados.
