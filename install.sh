#!/bin/bash

# Script de instalação do SaaS de Lip-Sync

echo "🚀 Instalação do SaaS de Geração de Vídeos com Lip-Sync"
echo "========================================================"
echo ""

# Verifica Python
echo "📦 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION encontrado"
echo ""

# Verifica FFmpeg
echo "🎬 Verificando FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg não encontrado"
    echo ""
    echo "Instale FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    exit 1
fi

FFMPEG_VERSION=$(ffmpeg -version | head -n1)
echo "✅ $FFMPEG_VERSION encontrado"
echo ""

# Cria ambiente virtual
echo "🐍 Criando ambiente virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi
echo ""

# Ativa ambiente virtual
echo "⚡ Ativando ambiente virtual..."
source venv/bin/activate
echo ""

# Instala dependências
echo "📚 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi
echo ""

# Verifica se .env existe
echo "🔑 Verificando configuração..."
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado"
    echo "📝 Copiando .env.example para .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione suas API keys:"
    echo "   - ELEVENLABS_API_KEY"
    echo "   - GEMINI_API_KEY"
    echo "   - WAVESPEED_API_KEY"
    echo ""
else
    echo "✅ Arquivo .env encontrado"
fi
echo ""

# Executa testes
echo "🧪 Executando testes de configuração..."
python test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Instalação concluída com sucesso!"
    echo ""
    echo "▶️  Para iniciar a aplicação:"
    echo "   source venv/bin/activate"
    echo "   python app.py"
else
    echo ""
    echo "⚠️  Instalação concluída com avisos"
    echo "   Verifique os erros acima e corrija antes de executar"
fi
