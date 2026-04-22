@echo off
echo Instalando dependencias...
pip install -r requirements.txt
pip install pyinstaller

echo Instalando navegadores do Playwright...
playwright install chromium

echo.
echo Compilando o executavel...
pyinstaller --noconfirm --onedir --windowed --name "Bot_Precos" app_gui.py

echo.
echo ========================================================
echo COMPILACAO CONCLUIDA!
echo.
echo O seu executavel esta localizado na pasta:
echo dist\Bot_Precos\Bot_Precos.exe
echo ========================================================
pause
