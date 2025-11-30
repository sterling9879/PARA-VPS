@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo 🚀 Instalacao do SaaS de Geracao de Videos com Lip-Sync
echo ========================================================
echo.

REM Verifica Python
echo 📦 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado. Por favor, instale Python 3.8+
    echo    Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% encontrado
echo.

REM Verifica FFmpeg
echo 🎬 Verificando FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ❌ FFmpeg nao encontrado
    echo.
    echo Instale FFmpeg:
    echo   1. Baixe de: https://ffmpeg.org/download.html
    echo   2. Extraia o arquivo
    echo   3. Adicione o caminho da pasta 'bin' ao PATH do sistema
    echo.
    echo Ou instale via Chocolatey:
    echo   choco install ffmpeg
    echo.
    pause
    exit /b 1
)

for /f "tokens=3" %%i in ('ffmpeg -version 2^>^&1 ^| findstr "ffmpeg version"') do (
    echo ✅ FFmpeg %%i encontrado
    goto :ffmpeg_found
)
:ffmpeg_found
echo.

REM Cria ambiente virtual
echo 🐍 Criando ambiente virtual...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Erro ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo ✅ Ambiente virtual criado
) else (
    echo ✅ Ambiente virtual ja existe
)
echo.

REM Ativa ambiente virtual
echo ⚡ Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Erro ao ativar ambiente virtual
    pause
    exit /b 1
)
echo.

REM Atualiza pip
echo 📦 Atualizando pip...
python -m pip install --upgrade pip --quiet
echo.

REM Instala dependências
echo 📚 Instalando dependencias...
echo    Isso pode levar alguns minutos...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Erro ao instalar dependencias
    echo.
    echo Tentando instalar novamente sem modo quiet...
    pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✅ Dependencias instaladas com sucesso
echo.

REM Verifica se .env existe
echo 🔑 Verificando configuracao...
if not exist ".env" (
    echo ⚠️  Arquivo .env nao encontrado
    echo 📝 Copiando .env.example para .env...
    copy .env.example .env >nul
    echo.
    echo ⚠️  IMPORTANTE: Edite o arquivo .env e adicione suas API keys:
    echo    - ELEVENLABS_API_KEY
    echo    - GEMINI_API_KEY
    echo    - WAVESPEED_API_KEY
    echo.
    echo Pressione qualquer tecla para abrir o .env no Notepad...
    pause >nul
    notepad .env
    echo.
) else (
    echo ✅ Arquivo .env encontrado
)
echo.

REM Executa testes
echo 🧪 Executando testes de configuracao...
python test_setup.py
set TEST_RESULT=!errorlevel!

echo.
if !TEST_RESULT! equ 0 (
    echo ========================================================
    echo 🎉 Instalacao concluida com sucesso!
    echo ========================================================
    echo.
    echo ▶️  Para iniciar a aplicacao:
    echo    1. Execute: start.bat
    echo    OU
    echo    2. Execute manualmente:
    echo       venv\Scripts\activate
    echo       python app.py
    echo.
) else (
    echo ========================================================
    echo ⚠️  Instalacao concluida com avisos
    echo ========================================================
    echo.
    echo Verifique os erros acima e corrija antes de executar
    echo.
)

pause
