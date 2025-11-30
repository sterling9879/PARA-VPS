#!/bin/bash
# =============================================================================
# Script de Instalacao da Aplicacao - LipSync Video Generator
# =============================================================================

set -e  # Sai em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Funções de log
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Configuracoes
APP_USER="lipsync"
APP_HOME="/home/$APP_USER"
APP_DIR="$APP_HOME/app"
REPO_URL="https://github.com/sterling9879/PARA-VPS.git"

echo ""
echo "============================================================================="
echo "       LipSync Video Generator - Instalacao da Aplicacao"
echo "============================================================================="
echo ""

# Verifica se está rodando como root ou usuario lipsync
if [ "$EUID" -eq 0 ]; then
    # Rodando como root, muda para usuario lipsync
    log_info "Rodando como root, executando como usuario $APP_USER..."

    # Executa este script como usuario lipsync
    sudo -u $APP_USER bash -c "cd $APP_DIR && $0"
    exit $?
fi

# Verifica se o usuario atual é o lipsync
if [ "$(whoami)" != "$APP_USER" ]; then
    log_error "Este script deve ser executado como usuario $APP_USER"
    log_info "Use: sudo -u $APP_USER bash install-app.sh"
    exit 1
fi

cd $APP_HOME

# =============================================================================
# 1. CLONAR OU ATUALIZAR REPOSITORIO
# =============================================================================
if [ -d "$APP_DIR/.git" ]; then
    log_info "Repositorio ja existe, atualizando..."
    cd $APP_DIR
    git fetch origin
    git pull origin main || git pull origin master || true
else
    log_info "Clonando repositorio..."
    if [ -d "$APP_DIR" ]; then
        rm -rf $APP_DIR
    fi
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

log_success "Repositorio pronto!"

# =============================================================================
# 2. CRIAR AMBIENTE VIRTUAL PYTHON
# =============================================================================
log_info "Criando ambiente virtual Python..."

if [ -d "$APP_DIR/venv" ]; then
    log_warn "Ambiente virtual ja existe, removendo..."
    rm -rf $APP_DIR/venv
fi

python3 -m venv $APP_DIR/venv
source $APP_DIR/venv/bin/activate

# Atualizar pip
pip install --upgrade pip wheel setuptools

log_success "Ambiente virtual criado!"

# =============================================================================
# 3. INSTALAR DEPENDENCIAS PYTHON
# =============================================================================
log_info "Instalando dependencias Python..."

if [ -f "$APP_DIR/requirements.txt" ]; then
    pip install -r $APP_DIR/requirements.txt
else
    log_warn "requirements.txt nao encontrado, instalando dependencias manualmente..."
    pip install \
        gradio==4.44.1 \
        google-generativeai==0.8.3 \
        python-dotenv==1.2.1 \
        requests==2.32.3 \
        Pillow==10.4.0 \
        Flask==3.0.0 \
        Flask-CORS==4.0.0 \
        Werkzeug==3.0.1
fi

log_success "Dependencias instaladas!"

# =============================================================================
# 4. CRIAR ARQUIVO .ENV (SE NAO EXISTIR)
# =============================================================================
if [ ! -f "$APP_DIR/.env" ]; then
    log_info "Criando arquivo .env a partir do exemplo..."

    if [ -f "$APP_DIR/.env.example" ]; then
        cp $APP_DIR/.env.example $APP_DIR/.env
        log_warn "IMPORTANTE: Edite o arquivo $APP_DIR/.env com suas API keys!"
    else
        log_info "Criando .env padrao..."
        cat > $APP_DIR/.env << 'EOF'
# API Keys - CONFIGURE ESTAS CHAVES!
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
WAVESPEED_API_KEY=
MINIMAX_API_KEY=

# Configuracoes
AUDIO_PROVIDER=elevenlabs
MAX_CONCURRENT_REQUESTS=10
BATCH_SIZE=3
POLL_INTERVAL=10.0
POLL_TIMEOUT=900.0
DEFAULT_RESOLUTION=480p
VIDEO_QUALITY=high
TEMP_FOLDER=./temp
EOF
        log_warn "IMPORTANTE: Edite o arquivo $APP_DIR/.env com suas API keys!"
    fi
else
    log_info "Arquivo .env ja existe"
fi

# Proteger arquivo .env
chmod 600 $APP_DIR/.env

# =============================================================================
# 5. CRIAR DIRETORIOS NECESSARIOS
# =============================================================================
log_info "Criando diretorios necessarios..."

mkdir -p $APP_DIR/temp/uploads
mkdir -p $APP_DIR/temp/outputs
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/data/avatars/thumbnails
mkdir -p $APP_DIR/static

log_success "Diretorios criados!"

# =============================================================================
# 6. VERIFICAR INSTALACAO
# =============================================================================
log_info "Verificando instalacao..."

# Verificar Python
PYTHON_VERSION=$(python3 --version 2>&1)
log_success "Python: $PYTHON_VERSION"

# Verificar FFmpeg
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -1)
    log_success "FFmpeg: $FFMPEG_VERSION"
else
    log_error "FFmpeg nao encontrado! Instale com: sudo apt install ffmpeg"
fi

# Verificar dependencias Python
log_info "Verificando modulos Python..."
python3 -c "import flask; print(f'Flask {flask.__version__}')" 2>/dev/null && log_success "Flask OK" || log_error "Flask nao instalado"
python3 -c "import dotenv; print('python-dotenv')" 2>/dev/null && log_success "python-dotenv OK" || log_error "python-dotenv nao instalado"
python3 -c "import requests; print(f'Requests {requests.__version__}')" 2>/dev/null && log_success "Requests OK" || log_error "Requests nao instalado"

# =============================================================================
# 7. CRIAR SCRIPT DE INICIALIZACAO
# =============================================================================
log_info "Criando script de inicializacao..."

cat > $APP_DIR/start.sh << 'EOF'
#!/bin/bash
# Script para iniciar a aplicacao

cd "$(dirname "$0")"

# Ativa ambiente virtual
source venv/bin/activate

# Define variaveis de ambiente
export FLASK_APP=web_server.py
export FLASK_ENV=production

# Inicia o servidor
echo "Iniciando LipSync Video Generator..."
echo "Acesse: http://0.0.0.0:5000"
python3 web_server.py
EOF

chmod +x $APP_DIR/start.sh

log_success "Script de inicializacao criado!"

# =============================================================================
# RESUMO
# =============================================================================
echo ""
echo "============================================================================="
echo "                    INSTALACAO COMPLETA!"
echo "============================================================================="
echo ""
echo "Diretorio da aplicacao: $APP_DIR"
echo ""
echo -e "${YELLOW}PROXIMOS PASSOS:${NC}"
echo ""
echo "1. Configure suas API keys:"
echo "   nano $APP_DIR/.env"
echo ""
echo "2. Teste a aplicacao manualmente:"
echo "   cd $APP_DIR"
echo "   source venv/bin/activate"
echo "   python3 web_server.py"
echo ""
echo "3. Configure o servico systemd (como root):"
echo "   sudo cp $APP_DIR/scripts/lipsync.service /etc/systemd/system/"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable lipsync"
echo "   sudo systemctl start lipsync"
echo ""
echo "4. Configure o Nginx (como root):"
echo "   sudo cp $APP_DIR/scripts/nginx-lipsync.conf /etc/nginx/sites-available/lipsync"
echo "   sudo ln -s /etc/nginx/sites-available/lipsync /etc/nginx/sites-enabled/"
echo "   sudo nginx -t"
echo "   sudo systemctl reload nginx"
echo ""
echo "============================================================================="
