# Compilando para .exe (Windows)

Para transformar este bot em um executável (`.exe`) para Windows, permitindo que qualquer pessoa o utilize sem precisar instalar o Python, siga estes passos:

## Requisitos no Windows

1. Ter o Python instalado no Windows.
2. Abrir o Prompt de Comando (CMD) ou PowerShell na pasta do projeto.

## Passos para Compilação

1. **Instalar as dependências e o PyInstaller**:
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   playwright install chromium
   ```

2. **Descobrir o caminho do Playwright**:
   O PyInstaller precisa saber onde o navegador Chromium do Playwright está instalado para empacotá-lo (ou você pode orientar o usuário a instalar via comando no primeiro uso). O comando abaixo embutirá os navegadores.

   ```cmd
   pyinstaller --noconfirm --onedir --windowed --add-data "<Caminho_do_Seu_Python>\Lib\site-packages\playwright;playwright/" app_gui.py
   ```
   *Nota: Substitua `<Caminho_do_Seu_Python>` pelo caminho real onde o Python/Playwright está instalado na sua máquina.*

   **Alternativa mais simples e leve (Recomendada):**
   Crie um executável mais leve que não embute o navegador, mas solicita a instalação no primeiro uso caso não exista.

   ```cmd
   pyinstaller --noconfirm --onedir --windowed --name "Bot_Precos_ML_Shopee" app_gui.py
   ```

3. **Garantir a Instalação do Playwright**:
   Como estamos gerando um `.exe`, para garantir que funcione em um PC "limpo", o app pode rodar `playwright install` via script na inicialização, ou você pode distribuir a pasta do navegador junto.

   No entanto, para o menor custo e complexidade, rode o comando acima para gerar a pasta `dist\Bot_Precos_ML_Shopee`.

4. **Distribuição**:
   - Vá até a pasta `dist` que foi criada.
   - Você verá a pasta `Bot_Precos_ML_Shopee`.
   - Compacte esta pasta em um arquivo `.zip` e envie para o usuário.
   - O usuário só precisará extrair e executar `Bot_Precos_ML_Shopee.exe`.
