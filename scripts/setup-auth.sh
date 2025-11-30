#!/bin/bash
# =============================================================================
# Script para Configurar Autenticacao Basica no Nginx
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
echo "       LipSync Video Generator - Configuracao de Autenticacao"
echo "============================================================================="
echo ""

# Verifica root
if [ "$EUID" -ne 0 ]; then
    log_error "Este script precisa ser executado como root (use sudo)"
    exit 1
fi

# =============================================================================
# 1. INSTALAR APACHE2-UTILS (para htpasswd)
# =============================================================================
log_info "Instalando ferramentas necessarias..."
apt-get install -y apache2-utils
log_success "Ferramentas instaladas!"

# =============================================================================
# 2. CRIAR USUARIO E SENHA
# =============================================================================
read -p "Digite o nome de usuario: " AUTH_USER

if [ -z "$AUTH_USER" ]; then
    log_error "Nome de usuario nao pode estar vazio"
    exit 1
fi

# Cria arquivo de senhas
HTPASSWD_FILE="/etc/nginx/.htpasswd"

if [ -f "$HTPASSWD_FILE" ]; then
    log_info "Adicionando usuario ao arquivo existente..."
    htpasswd $HTPASSWD_FILE $AUTH_USER
else
    log_info "Criando novo arquivo de senhas..."
    htpasswd -c $HTPASSWD_FILE $AUTH_USER
fi

# Protege o arquivo
chmod 640 $HTPASSWD_FILE
chown root:www-data $HTPASSWD_FILE

log_success "Usuario $AUTH_USER criado!"

# =============================================================================
# 3. ATUALIZAR NGINX PARA USAR AUTENTICACAO
# =============================================================================
log_info "Atualizando configuracao do Nginx..."

NGINX_CONF="/etc/nginx/sites-available/lipsync"

if [ ! -f "$NGINX_CONF" ]; then
    log_error "Arquivo de configuracao do Nginx nao encontrado!"
    exit 1
fi

# Verifica se ja tem autenticacao configurada
if grep -q "auth_basic" $NGINX_CONF; then
    log_warn "Autenticacao ja esta configurada no Nginx"
else
    log_info "Adicionando autenticacao..."

    # Adiciona autenticacao no bloco location /
    sed -i '/location \/ {/a\        auth_basic "Area Restrita - LipSync";\n        auth_basic_user_file /etc/nginx/.htpasswd;' $NGINX_CONF

    log_success "Autenticacao adicionada!"
fi

# Testa configuracao
nginx -t

# Recarrega Nginx
systemctl reload nginx

log_success "Nginx recarregado com autenticacao!"

# =============================================================================
# RESUMO
# =============================================================================
echo ""
echo "============================================================================="
echo "                    AUTENTICACAO CONFIGURADA!"
echo "============================================================================="
echo ""
echo "Usuario criado: $AUTH_USER"
echo ""
echo "Comandos uteis:"
echo "  - Adicionar usuario: sudo htpasswd /etc/nginx/.htpasswd novo_usuario"
echo "  - Remover usuario: sudo htpasswd -D /etc/nginx/.htpasswd usuario"
echo "  - Listar usuarios: sudo cat /etc/nginx/.htpasswd"
echo ""
echo "============================================================================="
