#!/bin/bash
# =============================================================================
# Script de Backup Automatico - LipSync Video Generator
# =============================================================================

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuracoes
BACKUP_DIR="/home/lipsync/backups"
APP_DIR="/home/lipsync/app"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_$DATE.tar.gz"
MAX_BACKUPS=7

echo -e "${GREEN}[BACKUP]${NC} Iniciando backup: $(date)"

# Cria diretorio de backup se nao existir
mkdir -p $BACKUP_DIR

# Verifica se o diretorio da app existe
if [ ! -d "$APP_DIR" ]; then
    echo -e "${YELLOW}[WARN]${NC} Diretorio da aplicacao nao encontrado: $APP_DIR"
    exit 1
fi

# Lista de arquivos/diretorios para backup
BACKUP_ITEMS=""

# Adiciona .env se existir
if [ -f "$APP_DIR/.env" ]; then
    BACKUP_ITEMS="$BACKUP_ITEMS $APP_DIR/.env"
fi

# Adiciona data/ se existir
if [ -d "$APP_DIR/data" ]; then
    BACKUP_ITEMS="$BACKUP_ITEMS $APP_DIR/data/"
fi

# Adiciona temp/outputs/ se existir (videos gerados)
if [ -d "$APP_DIR/temp/outputs" ]; then
    BACKUP_ITEMS="$BACKUP_ITEMS $APP_DIR/temp/outputs/"
fi

# Verifica se ha algo para backup
if [ -z "$BACKUP_ITEMS" ]; then
    echo -e "${YELLOW}[WARN]${NC} Nenhum arquivo para backup"
    exit 0
fi

# Cria o backup
echo -e "${GREEN}[BACKUP]${NC} Criando backup: $BACKUP_FILE"
tar -czvf $BACKUP_DIR/$BACKUP_FILE $BACKUP_ITEMS 2>/dev/null

# Verifica se o backup foi criado
if [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h $BACKUP_DIR/$BACKUP_FILE | cut -f1)
    echo -e "${GREEN}[BACKUP]${NC} Backup criado com sucesso!"
    echo -e "${GREEN}[BACKUP]${NC} Arquivo: $BACKUP_DIR/$BACKUP_FILE"
    echo -e "${GREEN}[BACKUP]${NC} Tamanho: $BACKUP_SIZE"
else
    echo -e "${YELLOW}[WARN]${NC} Falha ao criar backup"
    exit 1
fi

# Remove backups antigos (mantem apenas os ultimos MAX_BACKUPS)
echo -e "${GREEN}[BACKUP]${NC} Limpando backups antigos (mantendo ultimos $MAX_BACKUPS)..."
ls -t $BACKUP_DIR/backup_*.tar.gz 2>/dev/null | tail -n +$((MAX_BACKUPS + 1)) | xargs -r rm -v

# Lista backups existentes
echo -e "${GREEN}[BACKUP]${NC} Backups disponiveis:"
ls -lh $BACKUP_DIR/backup_*.tar.gz 2>/dev/null

echo -e "${GREEN}[BACKUP]${NC} Backup concluido: $(date)"
