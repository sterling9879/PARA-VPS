#!/bin/bash
# ============================================================================
# ZERO STUDIO - Script de Instalação Completa para VPS
# Sistema de Geração de Vídeos com Lip-Sync
# ============================================================================
#
# USO:
#   chmod +x INSTALL_VPS.sh
#   sudo ./INSTALL_VPS.sh
#
# O script irá pedir:
#   - Domínio (ex: zerostudiopessoal.online)
#   - Email para SSL
#   - Credenciais de login (usuário/senha)
#   - API Keys (ElevenLabs, Gemini, WaveSpeed)
#
# ============================================================================

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}============================================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}============================================================================${NC}"
    echo ""
}

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    print_error "Este script precisa ser executado como root (sudo)"
    exit 1
fi

# ============================================================================
# COLETA DE INFORMAÇÕES
# ============================================================================

print_header "ZERO STUDIO - Instalação Completa"

echo "Este script irá instalar e configurar o sistema completo."
echo ""

# Domínio
read -p "Digite o domínio (ex: zerostudiopessoal.online): " DOMAIN
if [ -z "$DOMAIN" ]; then
    print_error "Domínio é obrigatório!"
    exit 1
fi

# Email para SSL
read -p "Digite o email para certificado SSL: " SSL_EMAIL
if [ -z "$SSL_EMAIL" ]; then
    print_error "Email é obrigatório para o SSL!"
    exit 1
fi

# Credenciais de login
read -p "Digite o usuário para login [admin]: " AUTH_USER
AUTH_USER=${AUTH_USER:-admin}

read -s -p "Digite a senha para login: " AUTH_PASS
echo ""
if [ -z "$AUTH_PASS" ]; then
    print_error "Senha é obrigatória!"
    exit 1
fi

# API Keys
echo ""
print_status "Configuração das API Keys (pode deixar em branco e configurar depois)"
echo ""

read -p "ElevenLabs API Key: " ELEVENLABS_KEY
read -p "Gemini API Key: " GEMINI_KEY
read -p "WaveSpeed API Key: " WAVESPEED_KEY
read -p "MiniMax API Key (opcional): " MINIMAX_KEY

# Confirmação
echo ""
print_header "Confirme as configurações"
echo "Domínio: $DOMAIN"
echo "Email SSL: $SSL_EMAIL"
echo "Usuário: $AUTH_USER"
echo "Senha: ********"
echo "ElevenLabs: ${ELEVENLABS_KEY:+Configurada}"
echo "Gemini: ${GEMINI_KEY:+Configurada}"
echo "WaveSpeed: ${WAVESPEED_KEY:+Configurada}"
echo ""

read -p "Continuar com a instalação? (s/n): " CONFIRM
if [ "$CONFIRM" != "s" ] && [ "$CONFIRM" != "S" ]; then
    print_warning "Instalação cancelada."
    exit 0
fi

# ============================================================================
# 1. ATUALIZAÇÃO DO SISTEMA
# ============================================================================

print_header "1. Atualizando Sistema"

print_status "Atualizando pacotes..."
apt update && apt upgrade -y

print_success "Sistema atualizado!"

# ============================================================================
# 2. INSTALAÇÃO DE DEPENDÊNCIAS
# ============================================================================

print_header "2. Instalando Dependências"

print_status "Instalando Python 3.11 e dependências..."
apt install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

print_status "Instalando FFmpeg..."
apt install -y ffmpeg

print_status "Instalando Nginx..."
apt install -y nginx

print_status "Instalando Certbot para SSL..."
apt install -y certbot python3-certbot-nginx

print_status "Instalando Git..."
apt install -y git curl wget

print_success "Dependências instaladas!"

# ============================================================================
# 3. CRIAÇÃO DE USUÁRIO E DIRETÓRIOS
# ============================================================================

print_header "3. Configurando Usuário e Diretórios"

# Criar usuário se não existir
if ! id "lipsync" &>/dev/null; then
    print_status "Criando usuário lipsync..."
    useradd -m -s /bin/bash lipsync
fi

# Criar diretório da aplicação
APP_DIR="/home/lipsync/app"
print_status "Criando diretório da aplicação em $APP_DIR..."
mkdir -p $APP_DIR
chown -R lipsync:lipsync /home/lipsync

print_success "Usuário e diretórios configurados!"

# ============================================================================
# 4. CLONE DO REPOSITÓRIO
# ============================================================================

print_header "4. Baixando Aplicação"

cd $APP_DIR

# Se já existe, faz pull
if [ -d ".git" ]; then
    print_status "Repositório já existe, atualizando..."
    git config --global --add safe.directory $APP_DIR
    git fetch origin
    git checkout claude/setup-video-generation-vps-01Gn6naoCU4kVw3UqS1BFHmL 2>/dev/null || git checkout main
    git pull
else
    print_status "Clonando repositório..."
    # Usar o repositório do usuário
    git clone https://github.com/sterling9879/PARA-VPS.git .
    git config --global --add safe.directory $APP_DIR
    git checkout claude/setup-video-generation-vps-01Gn6naoCU4kVw3UqS1BFHmL 2>/dev/null || true
fi

chown -R lipsync:lipsync $APP_DIR

print_success "Aplicação baixada!"

# ============================================================================
# 5. AMBIENTE VIRTUAL E DEPENDÊNCIAS PYTHON
# ============================================================================

print_header "5. Configurando Ambiente Python"

cd $APP_DIR

print_status "Criando ambiente virtual..."
python3.11 -m venv venv

print_status "Instalando dependências Python..."
source venv/bin/activate

pip install --upgrade pip
pip install flask flask-cors python-dotenv requests elevenlabs google-generativeai werkzeug gunicorn

# Instalar requirements.txt se existir
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

deactivate

chown -R lipsync:lipsync $APP_DIR

print_success "Ambiente Python configurado!"

# ============================================================================
# 6. CONFIGURAÇÃO DO ARQUIVO .ENV
# ============================================================================

print_header "6. Configurando Variáveis de Ambiente"

cat > $APP_DIR/.env << EOF
# API Keys
ELEVENLABS_API_KEY=$ELEVENLABS_KEY
GEMINI_API_KEY=$GEMINI_KEY
WAVESPEED_API_KEY=$WAVESPEED_KEY
MINIMAX_API_KEY=$MINIMAX_KEY

# Autenticação
AUTH_EMAIL=$AUTH_USER
AUTH_PASSWORD=$AUTH_PASS

# Flask
FLASK_SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production

# Configurações
BATCH_SIZE=3
MAX_WORKERS=3
EOF

chown lipsync:lipsync $APP_DIR/.env
chmod 600 $APP_DIR/.env

print_success "Arquivo .env configurado!"

# ============================================================================
# 7. CRIAÇÃO DE DIRETÓRIOS NECESSÁRIOS
# ============================================================================

print_header "7. Criando Diretórios de Trabalho"

mkdir -p $APP_DIR/temp/uploads
mkdir -p $APP_DIR/temp/outputs
mkdir -p $APP_DIR/temp/audio
mkdir -p $APP_DIR/data/avatars/thumbnails
mkdir -p $APP_DIR/logs

chown -R lipsync:lipsync $APP_DIR

print_success "Diretórios criados!"

# ============================================================================
# 8. CONFIGURAÇÃO DO SYSTEMD
# ============================================================================

print_header "8. Configurando Serviço Systemd"

cat > /etc/systemd/system/lipsync.service << EOF
[Unit]
Description=LipSync Video Generator
After=network.target

[Service]
Type=simple
User=lipsync
Group=lipsync
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/python web_server.py
Restart=always
RestartSec=10

# Logs
StandardOutput=journal
StandardError=journal
SyslogIdentifier=lipsync

# Segurança
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

print_status "Recarregando systemd..."
systemctl daemon-reload

print_status "Habilitando serviço..."
systemctl enable lipsync

print_status "Iniciando serviço..."
systemctl start lipsync

# Verificar status
sleep 3
if systemctl is-active --quiet lipsync; then
    print_success "Serviço lipsync iniciado com sucesso!"
else
    print_warning "Serviço pode ter problemas. Verifique com: journalctl -u lipsync -f"
fi

# ============================================================================
# 9. CONFIGURAÇÃO DO NGINX
# ============================================================================

print_header "9. Configurando Nginx"

# Remover configuração default
rm -f /etc/nginx/sites-enabled/default

# Criar configuração do site
cat > /etc/nginx/sites-available/lipsync << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Logs
    access_log /var/log/nginx/lipsync_access.log;
    error_log /var/log/nginx/lipsync_error.log;

    # Tamanho máximo de upload
    client_max_body_size 100M;

    # Proxy para a aplicação Flask
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Arquivos estáticos
    location /static/ {
        alias $APP_DIR/static/;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Habilitar site
ln -sf /etc/nginx/sites-available/lipsync /etc/nginx/sites-enabled/

# Testar configuração
print_status "Testando configuração do Nginx..."
nginx -t

# Reiniciar Nginx
print_status "Reiniciando Nginx..."
systemctl restart nginx
systemctl enable nginx

print_success "Nginx configurado!"

# ============================================================================
# 10. CONFIGURAÇÃO DO SSL
# ============================================================================

print_header "10. Configurando SSL (Let's Encrypt)"

print_status "Obtendo certificado SSL para $DOMAIN..."

# Tentar obter certificado
certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m $SSL_EMAIL --redirect || {
    print_warning "Falha ao configurar SSL automaticamente."
    print_warning "Verifique se o domínio está apontando para este servidor."
    print_warning "Você pode tentar novamente com: certbot --nginx -d $DOMAIN"
}

# Configurar renovação automática
print_status "Configurando renovação automática do SSL..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

print_success "SSL configurado!"

# ============================================================================
# 11. CONFIGURAÇÃO DO FIREWALL
# ============================================================================

print_header "11. Configurando Firewall"

print_status "Configurando UFW..."
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw --force enable

print_success "Firewall configurado!"

# ============================================================================
# 12. FINALIZAÇÃO
# ============================================================================

print_header "INSTALAÇÃO CONCLUÍDA!"

echo ""
echo -e "${GREEN}Sistema instalado com sucesso!${NC}"
echo ""
echo "============================================================================"
echo "  INFORMAÇÕES DE ACESSO"
echo "============================================================================"
echo ""
echo -e "  URL: ${GREEN}https://$DOMAIN${NC}"
echo ""
echo -e "  Usuário: ${GREEN}$AUTH_USER${NC}"
echo -e "  Senha: ${GREEN}(a que você definiu)${NC}"
echo ""
echo "============================================================================"
echo "  COMANDOS ÚTEIS"
echo "============================================================================"
echo ""
echo "  Ver logs da aplicação:"
echo "    journalctl -u lipsync -f"
echo ""
echo "  Reiniciar aplicação:"
echo "    sudo systemctl restart lipsync"
echo ""
echo "  Status da aplicação:"
echo "    sudo systemctl status lipsync"
echo ""
echo "  Editar API Keys:"
echo "    nano $APP_DIR/.env"
echo "    sudo systemctl restart lipsync"
echo ""
echo "============================================================================"
echo ""

# Verificar status final
print_status "Verificando status dos serviços..."
echo ""

echo -n "Nginx: "
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}Rodando${NC}"
else
    echo -e "${RED}Parado${NC}"
fi

echo -n "LipSync: "
if systemctl is-active --quiet lipsync; then
    echo -e "${GREEN}Rodando${NC}"
else
    echo -e "${RED}Parado${NC}"
fi

echo ""
print_success "Instalação finalizada!"
