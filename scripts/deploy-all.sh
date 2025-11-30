#!/bin/bash
# =============================================================================
# Script de Deploy Completo - LipSync Video Generator
# Execute este script como root em uma VPS Ubuntu 22.04 limpa
# =============================================================================

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Banner
clear
echo -e "${CYAN}"
echo "============================================================================="
echo "    _      _       ____                   __     ___     _            "
echo "   | |    (_)_ __ / ___| _   _ _ __   ___ \\ \\   / (_) __| | ___  ___  "
echo "   | |    | | '_ \\\\___ \\| | | | '_ \\ / __| \\ \\ / /| |/ _\` |/ _ \\/ _ \\ "
echo "   | |___ | | |_) |___) | |_| | | | | (__   \\ V / | | (_| |  __/ (_) |"
echo "   |_____|_| .__/|____/ \\__, |_| |_|\\___|   \\_/  |_|\\__,_|\\___|\\___/ "
echo "           |_|          |___/                                         "
echo ""
echo "                    DEPLOY AUTOMATIZADO EM VPS"
echo "============================================================================="
echo -e "${NC}"

# Funcoes
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "\n${CYAN}==>${NC} ${GREEN}$1${NC}\n"; }

# Verificacoes iniciais
if [ "$EUID" -ne 0 ]; then
    log_error "Este script precisa ser executado como root"
    echo "Use: sudo bash deploy-all.sh"
    exit 1
fi

# Verifica sistema operacional
if ! grep -q "Ubuntu 22" /etc/os-release 2>/dev/null; then
    log_warn "Este script foi testado em Ubuntu 22.04"
    read -p "Deseja continuar mesmo assim? (s/n): " CONTINUE
    if [ "$CONTINUE" != "s" ]; then
        exit 1
    fi
fi

# Variaveis
APP_USER="lipsync"
APP_HOME="/home/$APP_USER"
APP_DIR="$APP_HOME/app"
REPO_URL="https://github.com/sterling9879/PARA-VPS.git"

# =============================================================================
log_step "ETAPA 1/8: Atualizando o Sistema"
# =============================================================================
apt-get update -y
apt-get upgrade -y
log_success "Sistema atualizado!"

# =============================================================================
log_step "ETAPA 2/8: Instalando Dependencias"
# =============================================================================
apt-get install -y \
    software-properties-common \
    build-essential \
    curl wget git unzip \
    htop nano vim \
    ufw fail2ban \
    ca-certificates gnupg \
    apache2-utils

# Python 3.10
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update -y
apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip

update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
update-alternatives --set python3 /usr/bin/python3.10

# FFmpeg
apt-get install -y ffmpeg

# Node.js e PM2
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs
npm install -g pm2

# Nginx e Certbot
apt-get install -y nginx certbot python3-certbot-nginx

log_success "Todas as dependencias instaladas!"

# =============================================================================
log_step "ETAPA 3/8: Configurando Usuario e Diretorios"
# =============================================================================
if ! id "$APP_USER" &>/dev/null; then
    useradd -m -s /bin/bash $APP_USER
    log_success "Usuario $APP_USER criado"
else
    log_warn "Usuario $APP_USER ja existe"
fi

mkdir -p $APP_DIR
chown -R $APP_USER:$APP_USER $APP_HOME
log_success "Diretorios configurados!"

# =============================================================================
log_step "ETAPA 4/8: Clonando e Instalando Aplicacao"
# =============================================================================
sudo -u $APP_USER bash << EOF
cd $APP_HOME

# Clone ou atualiza repositorio
if [ -d "$APP_DIR/.git" ]; then
    cd $APP_DIR
    git fetch origin
    git pull origin main || git pull origin master || true
else
    rm -rf $APP_DIR
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# Ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel setuptools
pip install -r requirements.txt

# Diretorios
mkdir -p temp/uploads temp/outputs logs data/avatars/thumbnails

# .env
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        cat > .env << 'ENVEOF'
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
WAVESPEED_API_KEY=
MINIMAX_API_KEY=
AUDIO_PROVIDER=elevenlabs
MAX_CONCURRENT_REQUESTS=10
BATCH_SIZE=3
TEMP_FOLDER=./temp
ENVEOF
    fi
fi
chmod 600 .env

# Script de inicio
cat > start.sh << 'STARTEOF'
#!/bin/bash
cd "\$(dirname "\$0")"
source venv/bin/activate
python3 web_server.py
STARTEOF
chmod +x start.sh
EOF

log_success "Aplicacao instalada!"

# =============================================================================
log_step "ETAPA 5/8: Configurando Systemd"
# =============================================================================
cat > /etc/systemd/system/lipsync.service << EOF
[Unit]
Description=LipSync Video Generator
After=network.target

[Service]
Type=simple
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=PYTHONUNBUFFERED=1
ExecStart=$APP_DIR/venv/bin/python3 web_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable lipsync
log_success "Servico systemd configurado!"

# =============================================================================
log_step "ETAPA 6/8: Configurando Nginx"
# =============================================================================
cat > /etc/nginx/sites-available/lipsync << 'NGINXEOF'
upstream lipsync_backend {
    server 127.0.0.1:5000;
    keepalive 32;
}

server {
    listen 80;
    listen [::]:80;
    server_name _;

    access_log /var/log/nginx/lipsync_access.log;
    error_log /var/log/nginx/lipsync_error.log;

    client_max_body_size 50M;

    location /static/ {
        alias /home/lipsync/app/static/;
        expires 7d;
    }

    location / {
        proxy_pass http://lipsync_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    location /api/generate/ {
        proxy_pass http://lipsync_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 60s;
        proxy_send_timeout 900s;
        proxy_read_timeout 900s;
    }

    location ~ /\. {
        deny all;
    }
}
NGINXEOF

rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/lipsync /etc/nginx/sites-enabled/
nginx -t
systemctl enable nginx
log_success "Nginx configurado!"

# =============================================================================
log_step "ETAPA 7/8: Configurando Firewall"
# =============================================================================
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 5000/tcp
ufw --force enable
log_success "Firewall configurado!"

# =============================================================================
log_step "ETAPA 8/8: Iniciando Servicos"
# =============================================================================
systemctl start lipsync
systemctl restart nginx
log_success "Servicos iniciados!"

# =============================================================================
# RESUMO FINAL
# =============================================================================
echo ""
echo -e "${GREEN}=============================================================================${NC}"
echo -e "${GREEN}                    DEPLOY CONCLUIDO COM SUCESSO!${NC}"
echo -e "${GREEN}=============================================================================${NC}"
echo ""
echo -e "  ${CYAN}Aplicacao:${NC}      LipSync Video Generator"
echo -e "  ${CYAN}Usuario:${NC}        $APP_USER"
echo -e "  ${CYAN}Diretorio:${NC}      $APP_DIR"
echo ""

# Obter IP
IP=$(curl -s ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')
echo -e "  ${GREEN}Acesse:${NC}         http://$IP"
echo ""
echo -e "${YELLOW}IMPORTANTE: Configure suas API keys!${NC}"
echo ""
echo "  1. Edite o arquivo .env:"
echo "     sudo nano $APP_DIR/.env"
echo ""
echo "  2. Adicione suas chaves:"
echo "     ELEVENLABS_API_KEY=sua_chave_aqui"
echo "     GEMINI_API_KEY=sua_chave_aqui"
echo "     WAVESPEED_API_KEY=sua_chave_aqui"
echo ""
echo "  3. Reinicie o servico:"
echo "     sudo systemctl restart lipsync"
echo ""
echo -e "${CYAN}Comandos uteis:${NC}"
echo "  - Status:    sudo systemctl status lipsync"
echo "  - Logs:      sudo journalctl -u lipsync -f"
echo "  - Reiniciar: sudo systemctl restart lipsync"
echo ""
echo -e "${GREEN}=============================================================================${NC}"
