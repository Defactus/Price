$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath ".\venv\Scripts\python.exe")) {
    python -m venv venv
}

.\venv\Scripts\python.exe -m pip install -r requirements.txt pyinstaller
$env:PLAYWRIGHT_BROWSERS_PATH = "0"
.\venv\Scripts\python.exe -m playwright install chromium
.\venv\Scripts\pyinstaller.exe --noconsole --onedir --name PriceComparer --exclude-module pytest app_gui.py

Write-Host "EXE gerado em: dist\PriceComparer\PriceComparer.exe"
