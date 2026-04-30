$ErrorActionPreference = "Stop"

$repoZipUrl = "https://github.com/Defactus/Price/archive/refs/heads/main.zip"
$installRoot = Join-Path $env:USERPROFILE "PriceComparer"
$zipPath = Join-Path $env:TEMP "PriceComparer-main.zip"
$extractPath = Join-Path $env:TEMP "PriceComparer-download"
$projectPath = Join-Path $extractPath "Price-main"
$desktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "Comparador de Precos.lnk"

Write-Host "Instalando Comparador de Precos sem Git..."

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "Python nao encontrado."
    Write-Host "Instale o Python em https://www.python.org/downloads/ e marque a opcao 'Add python.exe to PATH'."
    Write-Host "Depois execute este instalador novamente."
    exit 1
}

if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}

if (Test-Path -LiteralPath $extractPath) {
    Remove-Item -LiteralPath $extractPath -Recurse -Force
}

Write-Host "Baixando arquivos do projeto..."
Invoke-WebRequest -Uri $repoZipUrl -OutFile $zipPath

Write-Host "Extraindo arquivos..."
Expand-Archive -LiteralPath $zipPath -DestinationPath $extractPath -Force

if (Test-Path -LiteralPath $installRoot) {
    $backupPath = "$installRoot-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Write-Host "Instalacao anterior encontrada. Movendo para: $backupPath"
    Move-Item -LiteralPath $installRoot -Destination $backupPath
}

Move-Item -LiteralPath $projectPath -Destination $installRoot

Write-Host "Preparando o executavel. Esta etapa pode demorar alguns minutos..."
Set-Location -LiteralPath $installRoot
powershell -ExecutionPolicy Bypass -NoProfile -File ".\build_exe.ps1"

$exePath = Join-Path $installRoot "dist\PriceComparer\PriceComparer.exe"
if (-not (Test-Path -LiteralPath $exePath)) {
    throw "Nao foi possivel encontrar o executavel em: $exePath"
}

Write-Host "Criando atalho na Area de Trabalho..."
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($desktopShortcut)
$shortcut.TargetPath = $exePath
$shortcut.WorkingDirectory = Split-Path -Parent $exePath
$shortcut.Save()

Write-Host ""
Write-Host "Instalacao concluida."
Write-Host "Programa instalado em: $installRoot"
Write-Host "Executavel: $exePath"
Write-Host "Atalho criado em: $desktopShortcut"
