# Guia Completo de Deploy em VPS - LipSync Video Generator

Este guia detalha passo a passo como configurar e hospedar o sistema de geracao de videos com lip-sync em uma VPS Hostinger com Ubuntu 22.04.

## Indice

1. [Pre-requisitos](#pre-requisitos)
2. [Acesso a VPS](#acesso-a-vps)
3. [Setup Inicial do Servidor](#setup-inicial-do-servidor)
4. [Instalacao da Aplicacao](#instalacao-da-aplicacao)
5. [Configuracao das API Keys](#configuracao-das-api-keys)
6. [Configuracao do Systemd](#configuracao-do-systemd)
7. [Configuracao do Nginx](#configuracao-do-nginx)
8. [Configuracao de SSL](#configuracao-de-ssl)
9. [Seguranca](#seguranca)
10. [Monitoramento e Logs](#monitoramento-e-logs)
11. [Backup Automatico](#backup-automatico)
12. [Troubleshooting](#troubleshooting)
13. [Comandos Uteis](#comandos-uteis)

---

## Pre-requisitos

Antes de comecar, certifique-se de ter:

- [ ] VPS Hostinger com Ubuntu 22.04 instalado
- [ ] Acesso SSH a VPS (usuario e senha ou chave SSH)
- [ ] Dominio apontando para o IP da VPS (opcional, mas recomendado para SSL)
- [ ] Chaves de API dos servicos:
  - ElevenLabs
  - Google Gemini
  - WaveSpeed

---

## Acesso a VPS

### Via Terminal (Linux/Mac)

```bash
ssh root@SEU_IP_DA_VPS
```

### Via PuTTY (Windows)

1. Abra o PuTTY
2. Em "Host Name", digite o IP da VPS
3. Clique em "Open"
4. Digite o usuario (root) e senha

### Primeiro Acesso - Alterar Senha Root

```bash
# Altere a senha do root por seguranca
passwd
```

---

## Setup Inicial do Servidor

### Opcao 1: Script Automatizado (Recomendado)

```bash
# Baixe e execute o script de setup
cd /tmp
wget https://raw.githubusercontent.com/sterling9879/PARA-VPS/main/scripts/setup-server.sh
chmod +x setup-server.sh
sudo ./setup-server.sh
```

### Opcao 2: Instalacao Manual

Se preferir fazer manualmente, siga os passos:

#### 1. Atualizar o Sistema

```bash
sudo apt-get update -y
sudo apt-get upgrade -y
```

#### 2. Instalar Dependencias Basicas

```bash
sudo apt-get install -y \
    software-properties-common \
    build-essential \
    curl wget git unzip \
    htop nano vim \
    ufw fail2ban \
    ca-certificates gnupg
```

#### 3. Instalar Python 3.10+

```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update -y
sudo apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip

# Configurar como padrao
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --set python3 /usr/bin/python3.10

# Verificar
python3 --version  # Deve mostrar Python 3.10.x
```

#### 4. Instalar FFmpeg

```bash
sudo apt-get install -y ffmpeg

# Verificar
ffmpeg -version
```

#### 5. Instalar Node.js e PM2

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2
pm2 startup systemd
```

#### 6. Instalar Nginx

```bash
sudo apt-get install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

#### 7. Instalar Certbot (SSL)

```bash
sudo apt-get install -y certbot python3-certbot-nginx
```

#### 8. Criar Usuario da Aplicacao

```bash
# Criar usuario nao-root
sudo useradd -m -s /bin/bash lipsync
```

#### 9. Configurar Firewall

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 5000/tcp
sudo ufw --force enable

# Verificar
sudo ufw status
```

#### Verificar Setup

```bash
# Python
python3 --version

# FFmpeg
ffmpeg -version | head -1

# Node.js
node --version

# Nginx
nginx -v

# Firewall
sudo ufw status
```

---

## Instalacao da Aplicacao

### 1. Mudar para Usuario lipsync

```bash
sudo su - lipsync
cd ~
```

### 2. Clonar o Repositorio

```bash
git clone https://github.com/sterling9879/PARA-VPS.git app
cd app
```

### 3. Criar Ambiente Virtual Python

```bash
python3 -m venv venv
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip wheel setuptools
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Criar Diretorios Necessarios

```bash
mkdir -p temp/uploads temp/outputs logs data/avatars/thumbnails
```

### 6. Verificar Instalacao

```bash
# Dentro do ambiente virtual
python3 -c "import flask; print(f'Flask OK: {flask.__version__}')"
python3 -c "import requests; print(f'Requests OK: {requests.__version__}')"
```

---

## Configuracao das API Keys

### Onde Obter as Chaves

#### 1. ElevenLabs (Sintese de Voz)

1. Acesse: https://elevenlabs.io
2. Crie uma conta ou faca login
3. Va em: **Settings** > **API Keys**
4. Clique em **"Create API Key"**
5. Copie a chave (comeca com `sk_`)

**Planos:**
- Free: 10.000 caracteres/mes
- Starter: $5/mes - 30.000 caracteres/mes
- Creator: $22/mes - 100.000 caracteres/mes

#### 2. Google Gemini (Processamento de Texto)

1. Acesse: https://aistudio.google.com/app/apikey
2. Faca login com sua conta Google
3. Clique em **"Create API Key"**
4. Selecione ou crie um projeto
5. Copie a chave (comeca com `AIza`)

**Planos:**
- Gemini 2.5 Flash Lite: Gratuito com limites generosos

#### 3. WaveSpeed (Geracao de Video)

1. Acesse: https://wavespeed.ai
2. Crie uma conta
3. Acesse seu **Dashboard** ou **Profile**
4. Encontre a secao de API Keys
5. Copie sua chave

**Planos:**
- Pay-as-you-go: ~$0.20 por video

### Criar Arquivo .env

```bash
# Como usuario lipsync, no diretorio da aplicacao
cd /home/lipsync/app
cp .env.example .env
nano .env
```

Edite o arquivo com suas chaves:

```env
# API Keys - SUBSTITUA PELOS SEUS VALORES REAIS
ELEVENLABS_API_KEY=sk_sua_chave_elevenlabs_aqui
GEMINI_API_KEY=AIzaSua_chave_gemini_aqui
WAVESPEED_API_KEY=sua_chave_wavespeed_aqui

# Configuracoes (pode manter os valores padrao)
AUDIO_PROVIDER=elevenlabs
MAX_CONCURRENT_REQUESTS=10
BATCH_SIZE=3
TEMP_FOLDER=./temp
```

Salve com `Ctrl+X`, depois `Y`, depois `Enter`.

### Proteger o Arquivo .env

```bash
chmod 600 .env
```

### Testar a Aplicacao Manualmente

```bash
cd /home/lipsync/app
source venv/bin/activate
python3 web_server.py
```

Se tudo estiver correto, voce vera:
```
============================================================
  LipSync Video Generator - Web Interface
============================================================

  Acesse: http://localhost:5000
```

Pressione `Ctrl+C` para parar.

---

## Configuracao do Systemd

O systemd permite que a aplicacao rode automaticamente e reinicie em caso de falha.

### 1. Copiar Arquivo de Servico

```bash
# Como root
sudo cp /home/lipsync/app/scripts/lipsync.service /etc/systemd/system/
```

### 2. Recarregar Systemd

```bash
sudo systemctl daemon-reload
```

### 3. Habilitar e Iniciar Servico

```bash
sudo systemctl enable lipsync
sudo systemctl start lipsync
```

### 4. Verificar Status

```bash
sudo systemctl status lipsync
```

Deve mostrar:
```
● lipsync.service - LipSync Video Generator - Flask Web Server
     Active: active (running)
```

### Comandos Uteis do Systemd

```bash
# Ver status
sudo systemctl status lipsync

# Parar servico
sudo systemctl stop lipsync

# Iniciar servico
sudo systemctl start lipsync

# Reiniciar servico
sudo systemctl restart lipsync

# Ver logs em tempo real
sudo journalctl -u lipsync -f

# Ver ultimas 100 linhas de log
sudo journalctl -u lipsync -n 100
```

---

## Configuracao do Nginx

O Nginx atua como reverse proxy, melhorando seguranca e performance.

### 1. Copiar Configuracao

```bash
sudo cp /home/lipsync/app/scripts/nginx-lipsync.conf /etc/nginx/sites-available/lipsync
```

### 2. Habilitar Site

```bash
sudo ln -s /etc/nginx/sites-available/lipsync /etc/nginx/sites-enabled/
```

### 3. Remover Site Padrao (opcional)

```bash
sudo rm /etc/nginx/sites-enabled/default
```

### 4. Testar Configuracao

```bash
sudo nginx -t
```

Deve mostrar:
```
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 5. Recarregar Nginx

```bash
sudo systemctl reload nginx
```

### 6. Testar Acesso

Acesse no navegador:
```
http://SEU_IP_DA_VPS
```

---

## Configuracao de SSL

Para acessar via HTTPS (recomendado para producao).

### Pre-requisito

- Dominio configurado apontando para o IP da VPS
- Verificar propagacao DNS: `nslookup seudominio.com`

### Opcao 1: Script Automatizado

```bash
sudo /home/lipsync/app/scripts/setup-ssl.sh
```

### Opcao 2: Manual com Certbot

#### 1. Atualizar Nginx com Dominio

Edite `/etc/nginx/sites-available/lipsync`:
```bash
sudo nano /etc/nginx/sites-available/lipsync
```

Substitua `server_name _;` por:
```
server_name seudominio.com www.seudominio.com;
```

```bash
sudo nginx -t
sudo systemctl reload nginx
```

#### 2. Obter Certificado

```bash
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

Siga as instrucoes:
- Aceite os termos
- Informe seu email
- Escolha redirecionar HTTP para HTTPS (opcao 2)

#### 3. Verificar Renovacao Automatica

```bash
sudo certbot renew --dry-run
```

### Testar SSL

Acesse:
```
https://seudominio.com
```

Verifique o cadeado verde no navegador.

---

## Seguranca

### 1. Autenticacao Basica no Nginx

Proteja a interface com usuario e senha:

```bash
sudo /home/lipsync/app/scripts/setup-auth.sh
```

Ou manualmente:

```bash
# Instalar apache2-utils
sudo apt-get install -y apache2-utils

# Criar arquivo de senhas
sudo htpasswd -c /etc/nginx/.htpasswd admin

# Editar nginx config
sudo nano /etc/nginx/sites-available/lipsync
```

Adicione dentro do bloco `location / {`:
```nginx
auth_basic "Area Restrita";
auth_basic_user_file /etc/nginx/.htpasswd;
```

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 2. Fail2Ban

Ja instalado pelo script de setup. Para verificar:

```bash
sudo systemctl status fail2ban
```

### 3. Atualizacoes Automaticas

```bash
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 4. Desabilitar Login Root por SSH (Recomendado)

```bash
sudo nano /etc/ssh/sshd_config
```

Altere:
```
PermitRootLogin no
```

```bash
sudo systemctl restart sshd
```

**ATENCAO:** Antes de fazer isso, crie um usuario com sudo!

---

## Monitoramento e Logs

### Logs da Aplicacao

```bash
# Logs do systemd
sudo journalctl -u lipsync -f

# Logs do Nginx
sudo tail -f /var/log/nginx/lipsync_access.log
sudo tail -f /var/log/nginx/lipsync_error.log
```

### Monitoramento de Recursos

```bash
# Uso de CPU e memoria
htop

# Espaco em disco
df -h

# Uso de memoria
free -h
```

### Healthcheck

Acesse:
```
http://seudominio.com/health
```

Deve retornar: `OK`

---

## Backup Automatico

### Script de Backup

Crie o script:

```bash
sudo nano /home/lipsync/app/scripts/backup.sh
```

```bash
#!/bin/bash
# Script de Backup - LipSync Video Generator

BACKUP_DIR="/home/lipsync/backups"
APP_DIR="/home/lipsync/app"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup do .env e dados
tar -czvf $BACKUP_DIR/backup_$DATE.tar.gz \
    $APP_DIR/.env \
    $APP_DIR/data/ \
    $APP_DIR/temp/outputs/

# Manter apenas ultimos 7 backups
ls -t $BACKUP_DIR/backup_*.tar.gz | tail -n +8 | xargs -r rm

echo "Backup criado: $BACKUP_DIR/backup_$DATE.tar.gz"
```

```bash
chmod +x /home/lipsync/app/scripts/backup.sh
```

### Agendar Backup Automatico (Diario as 3h)

```bash
sudo crontab -e
```

Adicione:
```
0 3 * * * /home/lipsync/app/scripts/backup.sh >> /home/lipsync/app/logs/backup.log 2>&1
```

---

## Troubleshooting

### Problema: Aplicacao nao inicia

```bash
# Verificar logs
sudo journalctl -u lipsync -n 50

# Verificar se Python esta correto
/home/lipsync/app/venv/bin/python3 --version

# Testar manualmente
sudo su - lipsync
cd /home/lipsync/app
source venv/bin/activate
python3 web_server.py
```

### Problema: Erro 502 Bad Gateway

```bash
# Verificar se a aplicacao esta rodando
sudo systemctl status lipsync

# Verificar se a porta 5000 esta ocupada
sudo netstat -tlnp | grep 5000

# Reiniciar servicos
sudo systemctl restart lipsync
sudo systemctl restart nginx
```

### Problema: API key invalida

1. Verifique se as chaves estao corretas no arquivo `.env`
2. Verifique se nao ha espacos extras
3. Verifique se a conta da API esta ativa
4. Teste a chave manualmente:

```bash
# Testar ElevenLabs
curl -H "xi-api-key: SUA_CHAVE" https://api.elevenlabs.io/v1/user

# Testar Gemini
curl "https://generativelanguage.googleapis.com/v1/models?key=SUA_CHAVE"
```

### Problema: Permissao negada

```bash
# Corrigir permissoes
sudo chown -R lipsync:lipsync /home/lipsync/app
chmod 600 /home/lipsync/app/.env
chmod 755 /home/lipsync/app
```

### Problema: SSL nao funciona

```bash
# Verificar certificados
sudo certbot certificates

# Renovar manualmente
sudo certbot renew

# Verificar configuracao nginx
sudo nginx -t
```

---

## Comandos Uteis

### Gerenciamento do Servico

```bash
# Status
sudo systemctl status lipsync

# Reiniciar
sudo systemctl restart lipsync

# Logs em tempo real
sudo journalctl -u lipsync -f
```

### Atualizacao da Aplicacao

```bash
# Como usuario lipsync
sudo su - lipsync
cd /home/lipsync/app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
exit

# Como root, reiniciar servico
sudo systemctl restart lipsync
```

### Verificar Recursos

```bash
# CPU e Memoria
htop

# Disco
df -h

# Conexoes
sudo netstat -tlnp
```

### Nginx

```bash
# Testar config
sudo nginx -t

# Recarregar
sudo systemctl reload nginx

# Logs
sudo tail -f /var/log/nginx/lipsync_access.log
```

---

## Resumo Final

Apos seguir este guia, voce tera:

- [x] VPS Ubuntu 22.04 configurada e atualizada
- [x] Python 3.10+, FFmpeg, Node.js instalados
- [x] Aplicacao LipSync instalada e configurada
- [x] API keys configuradas no arquivo .env
- [x] Servico systemd rodando automaticamente
- [x] Nginx como reverse proxy
- [x] SSL com Let's Encrypt (se tiver dominio)
- [x] Autenticacao basica (opcional)
- [x] Firewall configurado
- [x] Backup automatico

**Acesso:**
- HTTP: `http://seu-ip-ou-dominio`
- HTTPS: `https://seudominio.com` (com SSL)

**Credenciais de teste:**
- Usuario: conforme configurado
- Senha: conforme configurado

---

## Suporte

Em caso de problemas:

1. Verifique os logs: `sudo journalctl -u lipsync -f`
2. Consulte a secao de Troubleshooting
3. Abra uma issue no GitHub

---

**Desenvolvido com dedicacao para facilitar o deploy em producao!**
