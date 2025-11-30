#!/bin/bash
# =============================================================================
# Script para Configurar SSL com Let's Encrypt
# =============================================================================

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[OK]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo ""
echo "============================================================================="
echo "       LipSync Video Generator - Configuracao de SSL"
echo "============================================================================="
echo ""

# Verifica root
if [ "$EUID" -ne 0 ]; then
    log_error "Este script precisa ser executado como root (use sudo)"
    exit 1
fi

# Solicita o dominio
read -p "Digite seu dominio (ex: meusite.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    log_error "Dominio nao pode estar vazio"
    exit 1
fi

# Solicita o email
read -p "Digite seu email (para notificacoes do Let's Encrypt): " EMAIL

if [ -z "$EMAIL" ]; then
    log_error "Email nao pode estar vazio"
    exit 1
fi

echo ""
log_info "Configurando SSL para: $DOMAIN"
log_info "Email de contato: $EMAIL"
echo ""

# =============================================================================
# 1. ATUALIZA CONFIGURACAO DO NGINX COM O DOMINIO
# =============================================================================
log_info "Atualizando configuracao do Nginx..."

NGINX_CONF="/etc/nginx/sites-available/lipsync"

if [ -f "$NGINX_CONF" ]; then
    # Substitui server_name
    sed -i "s/server_name _;/server_name $DOMAIN www.$DOMAIN;/g" $NGINX_CONF
    log_success "Configuracao do Nginx atualizada"
else
    log_error "Arquivo de configuracao do Nginx nao encontrado!"
    log_info "Execute primeiro: sudo cp /home/lipsync/app/scripts/nginx-lipsync.conf /etc/nginx/sites-available/lipsync"
    exit 1
fi

# Testa configuracao
nginx -t

# Recarrega Nginx
systemctl reload nginx
log_success "Nginx recarregado"

# =============================================================================
# 2. OBTER CERTIFICADO SSL
# =============================================================================
log_info "Obtendo certificado SSL com Certbot..."

# Cria diretorio para webroot
mkdir -p /var/www/certbot

# Obtem certificado
certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

log_success "Certificado SSL obtido!"

# =============================================================================
# 3. ATUALIZAR NGINX PARA HTTPS
# =============================================================================
log_info "Atualizando Nginx para HTTPS..."

# Cria nova configuracao com HTTPS
cat > $NGINX_CONF << EOF
# =============================================================================
# Nginx Configuration - LipSync Video Generator (HTTPS)
# =============================================================================

limit_req_zone \$binary_remote_addr zone=lipsync_limit:10m rate=10r/s;
limit_conn_zone \$binary_remote_addr zone=lipsync_conn:10m;

upstream lipsync_backend {
    server 127.0.0.1:5000;
    keepalive 32;
}

# Redireciona HTTP para HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN www.$DOMAIN;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# Servidor HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;

    # Certificados SSL
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

    # Configuracoes SSL modernas
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;

    # Logs
    access_log /var/log/nginx/lipsync_access.log;
    error_log /var/log/nginx/lipsync_error.log;

    # Seguranca headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Tamanho maximo de upload
    client_max_body_size 50M;
    client_body_timeout 120s;

    # Rate limiting
    limit_req zone=lipsync_limit burst=20 nodelay;
    limit_conn lipsync_conn 10;

    # Arquivos estaticos
    location /static/ {
        alias /home/lipsync/app/static/;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy para Flask
    location / {
        proxy_pass http://lipsync_backend;
        proxy_http_version 1.1;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Connection "";

        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    # API de geracao - timeout maior
    location /api/generate/ {
        proxy_pass http://lipsync_backend;
        proxy_http_version 1.1;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        proxy_connect_timeout 60s;
        proxy_send_timeout 900s;
        proxy_read_timeout 900s;
    }

    # Download de videos
    location /api/download/ {
        proxy_pass http://lipsync_backend;
        proxy_http_version 1.1;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

        proxy_buffering off;
        proxy_read_timeout 300s;
    }

    # Stream de videos
    location /api/stream/ {
        proxy_pass http://lipsync_backend;
        proxy_http_version 1.1;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

        proxy_buffering off;
    }

    # Upload
    location /api/upload/ {
        proxy_pass http://lipsync_backend;
        proxy_http_version 1.1;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

        client_max_body_size 50M;
        proxy_request_buffering off;
    }

    # Health check
    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }

    # Bloqueia arquivos sensiveis
    location ~ /\. {
        deny all;
    }
}
EOF

# Testa e recarrega
nginx -t
systemctl reload nginx

log_success "Nginx configurado com HTTPS!"

# =============================================================================
# 4. CONFIGURAR RENOVACAO AUTOMATICA
# =============================================================================
log_info "Configurando renovacao automatica do certificado..."

# Adiciona cron job para renovacao
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet && systemctl reload nginx") | crontab -

log_success "Renovacao automatica configurada!"

# =============================================================================
# RESUMO
# =============================================================================
echo ""
echo "============================================================================="
echo "                    SSL CONFIGURADO COM SUCESSO!"
echo "============================================================================="
echo ""
echo "Seu site agora esta acessivel em:"
echo "  https://$DOMAIN"
echo ""
echo "O certificado sera renovado automaticamente."
echo ""
echo "============================================================================="
