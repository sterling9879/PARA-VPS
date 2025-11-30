@echo off
color 0A
title LipSync Video Generator - Web Interface

:: Banner
cls
echo.
echo ================================================================
echo.
echo      LipSync Video Generator - Web Interface
echo.
echo      Sistema Profissional de Ger

acao de Videos com IA
echo.
echo ================================================================
echo.
echo.

:: Verifica se Python esta instalado
echo [1/3] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.8+ de: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)
echo [OK] Python encontrado
echo.

:: Verifica se o .env existe
echo [2/3] Verificando configuracoes...
if not exist .env (
    color 0E
    echo.
    echo [AVISO] Arquivo .env nao encontrado!
    echo.
    echo Criando a partir do .env.example...
    copy .env.example .env >nul
    echo.
    echo [OK] Arquivo .env criado
    echo.
    echo [IMPORTANTE] Configure suas API Keys pela interface web!
    echo.
    timeout /t 2 >nul
)
echo [OK] Configuracoes OK
echo.

:: Verifica se os assets foram criados
echo [3/3] Verificando assets...
if not exist projects\\metadata.json (
    color 0E
    echo.
    echo [AVISO] Assets nao encontrados!
    echo.
    echo Executando setup inicial...
    python setup_assets.py
    echo.
    echo [OK] Assets criados
    echo.
) else (
    echo [OK] Assets OK
)
echo.

:: Inicia interface web
cls
echo.
echo ================================================================
echo.
echo   Iniciando Interface Web Moderna...
echo.
echo   [OK] API REST
echo   [OK] Frontend Moderno
echo   [OK] Configuracao de API Keys
echo   [OK] Sistema de Projetos
echo   [OK] Biblioteca de Avatares
echo.
echo   Acesse: http://localhost:5000
echo.
echo ================================================================
echo.
echo.
color 0B
python web_server.py

:: Tratamento de erros
if errorlevel 1 (
    color 0C
    echo.
    echo [ERRO] Erro ao executar a aplicacao!
    echo.
    echo Verifique:
    echo   - Se todas as dependencias foram instaladas: pip install -r requirements.txt
    echo   - Se ha erros no terminal acima
    echo.
)

pause
