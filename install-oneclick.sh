#!/bin/bash
# =============================================================================
# LipSync Video Generator - Instalacao com 1 Clique
# VPS Ubuntu 22.04
# =============================================================================

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo -e "${CYAN}=============================================================================${NC}"
echo -e "${CYAN}       LipSync Video Generator - Instalacao com 1 Clique${NC}"
echo -e "${CYAN}=============================================================================${NC}"
echo ""

# Verifica root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[ERRO]${NC} Execute como root: sudo bash install-oneclick.sh"
    exit 1
fi

# Evita prompts interativos
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a

APP_USER="lipsync"
APP_HOME="/home/$APP_USER"
APP_DIR="$APP_HOME/app"
REPO_URL="https://github.com/sterling9879/PARA-VPS.git"

echo -e "${BLUE}[1/6]${NC} Atualizando sistema..."
apt-get update -y
apt-get -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade -y

echo -e "${BLUE}[2/6]${NC} Instalando dependencias..."
apt-get install -y software-properties-common build-essential curl wget git unzip htop nano ufw fail2ban ca-certificates gnupg lsb-release ffmpeg nginx certbot python3-certbot-nginx

# Python 3.10
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update -y
apt-get install -y python3.10 python3.10-venv python3.10-dev python3-pip
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 2>/dev/null || true
python3 -m pip install --upgrade pip

echo -e "${BLUE}[3/6]${NC} Configurando firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 5000/tcp
ufw --force enable

echo -e "${BLUE}[4/6]${NC} Criando usuario e estrutura..."
if ! id "$APP_USER" &>/dev/null; then
    useradd -m -s /bin/bash $APP_USER
fi
mkdir -p $APP_DIR
chown -R $APP_USER:$APP_USER $APP_HOME

echo -e "${BLUE}[5/6]${NC} Instalando aplicacao..."
cd $APP_HOME

# Clone ou update
if [ -d "$APP_DIR/.git" ]; then
    cd $APP_DIR
    sudo -u $APP_USER git fetch origin
    sudo -u $APP_USER git pull origin main || sudo -u $APP_USER git pull origin master || true
else
    rm -rf $APP_DIR
    sudo -u $APP_USER git clone $REPO_URL $APP_DIR
fi

cd $APP_DIR

# Ambiente virtual
sudo -u $APP_USER python3 -m venv $APP_DIR/venv
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip wheel setuptools
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt

# Criar .env se nao existir
if [ ! -f "$APP_DIR/.env" ]; then
    cat > $APP_DIR/.env << 'EOF'
# API Keys - Configure pelo frontend
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
WAVESPEED_API_KEY=
MINIMAX_API_KEY=

# Credenciais Padrao
AUTH_EMAIL=admin
AUTH_PASSWORD=admin123

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
    chown $APP_USER:$APP_USER $APP_DIR/.env
    chmod 600 $APP_DIR/.env
fi

# Criar diretorios
sudo -u $APP_USER mkdir -p $APP_DIR/temp/uploads $APP_DIR/temp/outputs $APP_DIR/logs $APP_DIR/data/avatars/thumbnails

echo -e "${BLUE}[6/6]${NC} Configurando servicos..."

# Systemd service
cat > /etc/systemd/system/lipsync.service << EOF
[Unit]
Description=LipSync Video Generator
After=network.target

[Service]
Type=simple
User=$APP_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/python web_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable lipsync
systemctl start lipsync

# Nginx basico
cat > /etc/nginx/sites-available/lipsync << 'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
    }
}
EOF

ln -sf /etc/nginx/sites-available/lipsync /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# =============================================================================
# FINALIZADO
# =============================================================================
echo ""
echo -e "${GREEN}=============================================================================${NC}"
echo -e "${GREEN}                    INSTALACAO CONCLUIDA!${NC}"
echo -e "${GREEN}=============================================================================${NC}"
echo ""
echo -e "Acesse: ${CYAN}http://SEU_IP${NC}"
echo ""
echo -e "${YELLOW}CREDENCIAIS PADRAO:${NC}"
echo -e "  Usuario: ${CYAN}admin${NC}"
echo -e "  Senha:   ${CYAN}admin123${NC}"
echo ""
echo -e "${RED}IMPORTANTE:${NC}"
echo "  1. Altere a senha no primeiro acesso"
echo "  2. Configure as API keys em 'Configuracoes'"
echo "  3. Para HTTPS, execute: bash $APP_DIR/scripts/setup-ssl.sh"
echo ""
echo -e "${GREEN}=============================================================================${NC}"
