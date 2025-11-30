@echo off
REM Script para testar a configuracao do sistema

echo ========================================================
echo 🧪 Testando Configuracao do Sistema
echo ========================================================
echo.

REM Verifica se ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual nao encontrado!
    echo.
    echo Execute primeiro: install.bat
    echo.
    pause
    exit /b 1
)

REM Ativa ambiente virtual
call venv\Scripts\activate.bat

REM Executa testes
python test_setup.py

echo.
pause
