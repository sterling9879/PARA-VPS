#!/bin/bash

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
clear
echo -e "${CYAN}"
echo "████████████████████████████████████████████████████████████████"
echo "█                                                              █"
echo "█     🎬 LipSync Video Generator Pro v2.0                     █"
echo "█                                                              █"
echo "█     Sistema Profissional de Geração de Vídeos com IA        █"
echo "█                                                              █"
echo "████████████████████████████████████████████████████████████████"
echo -e "${NC}"
echo ""

# Função para verificar Python
check_python() {
    echo -e "${BLUE}[1/5] 🔍 Verificando Python...${NC}"
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}"
        echo "❌ ERRO: Python 3 não encontrado!"
        echo ""
        echo "Por favor, instale Python 3.8+ de: https://www.python.org/downloads/"
        echo -e "${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Python encontrado${NC}"
    echo ""
}

# Função para verificar .env
check_env() {
    echo -e "${BLUE}[2/5] 🔍 Verificando configurações...${NC}"
    if [ ! -f .env ]; then
        echo -e "${YELLOW}"
        echo "⚠️  AVISO: Arquivo .env não encontrado!"
        echo ""
        echo "Criando a partir do .env.example..."
        cp .env.example .env
        echo ""
        echo "✅ Arquivo .env criado"
        echo ""
        echo "📝 IMPORTANTE: Edite o arquivo .env e adicione suas API Keys!"
        echo ""
        echo "Pressione ENTER para abrir o .env no editor..."
        echo -e "${NC}"
        read
        ${EDITOR:-nano} .env
        echo ""
    fi
    echo -e "${GREEN}✅ Configurações OK${NC}"
    echo ""
}

# Função para verificar dependências
check_dependencies() {
    echo -e "${BLUE}[3/5] 📦 Verificando dependências...${NC}"
    if ! python3 -c "import gradio" &> /dev/null; then
        echo -e "${YELLOW}"
        echo "⚠️  Dependências não instaladas!"
        echo ""
        read -p "Deseja instalar agora? (s/N): " install_deps
        if [[ $install_deps =~ ^[Ss]$ ]]; then
            echo ""
            echo "📥 Instalando dependências..."
            pip3 install -r requirements.txt
            echo ""
            echo -e "${GREEN}✅ Dependências instaladas${NC}"
        else
            echo ""
            echo -e "${RED}❌ Não é possível continuar sem as dependências${NC}"
            exit 1
        fi
        echo -e "${NC}"
    fi
    echo -e "${GREEN}✅ Dependências OK${NC}"
    echo ""
}

# Função para verificar assets
check_assets() {
    echo -e "${BLUE}[4/5] 🎭 Verificando assets...${NC}"
    if [ ! -f projects/metadata.json ]; then
        echo -e "${YELLOW}"
        echo "⚠️  Assets não encontrados!"
        echo ""
        echo "Executando setup inicial..."
        python3 setup_assets.py
        echo ""
        echo -e "${GREEN}✅ Assets criados${NC}"
        echo -e "${NC}"
    else
        echo -e "${GREEN}✅ Assets OK${NC}"
    fi
    echo ""
}

# Função de menu
show_menu() {
    clear
    echo -e "${CYAN}"
    echo "████████████████████████████████████████████████████████████████"
    echo "█                                                              █"
    echo "█     🎬 LipSync Video Generator Pro v2.0                     █"
    echo "█                                                              █"
    echo "████████████████████████████████████████████████████████████████"
    echo -e "${NC}"
    echo ""
    echo -e "${BLUE}[5/5] 🚀 Selecione a interface:${NC}"
    echo ""
    echo "    [1] 🌟 Interface Profissional (app_pro.py) - RECOMENDADO"
    echo "        └─ Dashboard, Projetos, Logs em tempo real"
    echo ""
    echo "    [2] 📋 Interface Original (app.py)"
    echo "        └─ Interface clássica com tabs"
    echo ""
    echo "    [3] 🖥️  Interface GUI Nativa (app_gui.py)"
    echo "        └─ Aplicação desktop (PyQt5)"
    echo ""
    echo "    [4] ⚙️  Executar Setup de Assets"
    echo "        └─ Recria avatares e templates"
    echo ""
    echo "    [5] ❌ Sair"
    echo ""
    echo ""
    read -p "Digite sua escolha (1-5): " choice
    
    case $choice in
        1) start_pro ;;
        2) start_original ;;
        3) start_gui ;;
        4) run_setup ;;
        5) exit 0 ;;
        *) 
            echo ""
            echo -e "${RED}❌ Opção inválida! Tente novamente.${NC}"
            sleep 2
            show_menu
            ;;
    esac
}

# Função para iniciar interface profissional
start_pro() {
    clear
    echo ""
    echo -e "${CYAN}████████████████████████████████████████████████████████████████${NC}"
    echo ""
    echo "  🌟 Iniciando Interface Profissional..."
    echo ""
    echo "  📊 Dashboard    ✓"
    echo "  📁 Projetos     ✓"
    echo "  🎬 Gerador      ✓"
    echo "  💻 Logs         ✓"
    echo ""
    echo "  Acesse: http://localhost:7860"
    echo ""
    echo -e "${CYAN}████████████████████████████████████████████████████████████████${NC}"
    echo ""
    echo ""
    python3 app_pro.py
    handle_exit $?
}

# Função para iniciar interface original
start_original() {
    clear
    echo ""
    echo -e "${CYAN}████████████████████████████████████████████████████████████████${NC}"
    echo ""
    echo "  📋 Iniciando Interface Original..."
    echo ""
    echo "  🎬 Vídeo Único           ✓"
    echo "  📚 Processamento Lote    ✓"
    echo ""
    echo "  Acesse: http://localhost:7860"
    echo ""
    echo -e "${CYAN}████████████████████████████████████████████████████████████████${NC}"
    echo ""
    echo ""
    python3 app.py
    handle_exit $?
}

# Função para iniciar GUI
start_gui() {
    clear
    echo ""
    echo -e "${CYAN}████████████████████████████████████████████████████████████████${NC}"
    echo ""
    echo "  🖥️  Iniciando Interface GUI Nativa..."
    echo ""
    echo "  Aplicação desktop será aberta em uma nova janela"
    echo ""
    echo -e "${CYAN}████████████████████████████████████████████████████████████████${NC}"
    echo ""
    echo ""
    python3 app_gui.py
    handle_exit $?
}

# Função para executar setup
run_setup() {
    clear
    echo ""
    echo -e "${CYAN}████████████████████████████████████████████████████████████████${NC}"
    echo ""
    echo "  ⚙️  Executando Setup de Assets..."
    echo ""
    echo -e "${CYAN}████████████████████████████████████████████████████████████████${NC}"
    echo ""
    echo ""
    python3 setup_assets.py
    echo ""
    echo ""
    echo -e "${GREEN}✅ Setup concluído!${NC}"
    echo ""
    read -p "Pressione ENTER para continuar..."
    show_menu
}

# Função para tratar saída
handle_exit() {
    echo ""
    echo ""
    if [ $1 -ne 0 ]; then
        echo -e "${RED}"
        echo "❌ Erro ao executar a aplicação!"
        echo ""
        echo "Verifique:"
        echo "  - Se todas as API Keys estão configuradas no .env"
        echo "  - Se as dependências foram instaladas corretamente"
        echo "  - Se há erros no terminal acima"
        echo -e "${NC}"
    else
        echo -e "${GREEN}"
        echo "✅ Aplicação encerrada com sucesso!"
        echo -e "${NC}"
    fi
    echo ""
    read -p "Pressione ENTER para voltar ao menu..."
    show_menu
}

# Execução principal
check_python
check_env
check_dependencies
check_assets
show_menu
