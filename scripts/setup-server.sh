#!/bin/bash
# =============================================================================
# Script de Setup Inicial do Servidor - VPS Ubuntu 22.04
# LipSync Video Generator
# =============================================================================

set -e  # Sai em caso de erro

# Evita prompts interativos durante instalacao (kernel, grub, etc)
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo ""
echo "============================================================================="
echo "       LipSync Video Generator - Setup do Servidor VPS"
echo "============================================================================="
echo ""

# Verifica se está rodando como root
if [ "$EUID" -ne 0 ]; then
    log_error "Este script precisa ser executado como root (use sudo)"
    exit 1
fi

# =============================================================================
# 1. ATUALIZAR O SISTEMA
# =============================================================================
log_info "Atualizando o sistema..."

# Configura para manter configuracoes atuais automaticamente
apt-get update -y
apt-get -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade -y
log_success "Sistema atualizado!"

# =============================================================================
# 2. INSTALAR DEPENDENCIAS BASICAS
# =============================================================================
log_info "Instalando dependencias basicas..."
apt-get install -y \
    software-properties-common \
    build-essential \
    curl \
    wget \
    git \
    unzip \
    htop \
    nano \
    vim \
    ufw \
    fail2ban \
    ca-certificates \
    gnupg \
    lsb-release

log_success "Dependencias basicas instaladas!"

# =============================================================================
# 3. INSTALAR PYTHON 3.10+
# =============================================================================
log_info "Instalando Python 3.10..."
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update -y
apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip

# Configurar Python 3.10 como padrao
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
update-alternatives --set python3 /usr/bin/python3.10

# Atualizar pip
python3 -m pip install --upgrade pip

log_success "Python 3.10 instalado!"
python3 --version

# =============================================================================
# 4. INSTALAR FFMPEG
# =============================================================================
log_info "Instalando FFmpeg..."
apt-get install -y ffmpeg
log_success "FFmpeg instalado!"
ffmpeg -version | head -1

# =============================================================================
# 5. INSTALAR NODE.JS E PM2 (para gerenciamento de processos)
# =============================================================================
log_info "Instalando Node.js e PM2..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
npm install -g pm2
pm2 startup systemd
log_success "Node.js e PM2 instalados!"

# =============================================================================
# 6. INSTALAR NGINX
# =============================================================================
log_info "Instalando Nginx..."
apt-get install -y nginx
systemctl enable nginx
systemctl start nginx
log_success "Nginx instalado e iniciado!"

# =============================================================================
# 7. INSTALAR CERTBOT (para SSL)
# =============================================================================
log_info "Instalando Certbot para SSL..."
apt-get install -y certbot python3-certbot-nginx
log_success "Certbot instalado!"

# =============================================================================
# 8. CRIAR USUARIO NAO-ROOT PARA A APLICACAO
# =============================================================================
APP_USER="lipsync"
APP_HOME="/home/$APP_USER"

if id "$APP_USER" &>/dev/null; then
    log_warn "Usuario $APP_USER ja existe"
else
    log_info "Criando usuario $APP_USER..."
    useradd -m -s /bin/bash $APP_USER
    log_success "Usuario $APP_USER criado!"
fi

# =============================================================================
# 9. CONFIGURAR FIREWALL (UFW)
# =============================================================================
log_info "Configurando firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 5000/tcp    # Flask
ufw allow 7860/tcp    # Gradio (se usar)
ufw --force enable
log_success "Firewall configurado!"
ufw status

# =============================================================================
# 10. CONFIGURAR FAIL2BAN
# =============================================================================
log_info "Configurando Fail2Ban..."
systemctl enable fail2ban
systemctl start fail2ban
log_success "Fail2Ban configurado!"

# =============================================================================
# 11. CRIAR ESTRUTURA DE DIRETORIOS
# =============================================================================
APP_DIR="$APP_HOME/app"
log_info "Criando estrutura de diretorios em $APP_DIR..."

mkdir -p $APP_DIR
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/backups
mkdir -p $APP_DIR/temp

chown -R $APP_USER:$APP_USER $APP_HOME
chmod 755 $APP_HOME

log_success "Estrutura de diretorios criada!"

# =============================================================================
# RESUMO
# =============================================================================
echo ""
echo "============================================================================="
echo "                    SETUP INICIAL COMPLETO!"
echo "============================================================================="
echo ""
echo "Componentes instalados:"
echo "  - Python $(python3 --version 2>&1 | cut -d' ' -f2)"
echo "  - FFmpeg $(ffmpeg -version 2>&1 | head -1 | cut -d' ' -f3)"
echo "  - Node.js $(node --version)"
echo "  - PM2 $(pm2 --version)"
echo "  - Nginx $(nginx -v 2>&1 | cut -d'/' -f2)"
echo "  - Certbot (para SSL)"
echo ""
echo "Usuario da aplicacao: $APP_USER"
echo "Diretorio da aplicacao: $APP_DIR"
echo ""
echo "Portas abertas no firewall:"
echo "  - 22 (SSH)"
echo "  - 80 (HTTP)"
echo "  - 443 (HTTPS)"
echo "  - 5000 (Flask)"
echo "  - 7860 (Gradio)"
echo ""
echo "Proximo passo: Execute o script install-app.sh"
echo "============================================================================="
