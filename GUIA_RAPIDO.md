# ZERO STUDIO - Guia Rápido de Instalação

## Pré-requisitos

1. VPS Ubuntu 22.04 (mínimo 2GB RAM)
2. Domínio apontando para o IP do servidor
3. Acesso root ao servidor

## Instalação Rápida

### 1. Conecte no servidor via SSH

```bash
ssh root@SEU_IP
```

### 2. Baixe e execute o script de instalação

```bash
# Baixar o script
wget https://raw.githubusercontent.com/sterling9879/PARA-VPS/claude/setup-video-generation-vps-01Gn6naoCU4kVw3UqS1BFHmL/INSTALL_VPS.sh

# Dar permissão de execução
chmod +x INSTALL_VPS.sh

# Executar
sudo ./INSTALL_VPS.sh
```

### 3. O script vai pedir:

- **Domínio**: seu domínio (ex: zerostudiopessoal.online)
- **Email**: para o certificado SSL
- **Usuário/Senha**: credenciais de login no sistema
- **API Keys**: ElevenLabs, Gemini, WaveSpeed (pode configurar depois)

## Instalação Manual (Passo a Passo)

Se preferir instalar manualmente:

### 1. Atualizar sistema
```bash
apt update && apt upgrade -y
```

### 2. Instalar dependências
```bash
apt install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
apt install -y ffmpeg nginx certbot python3-certbot-nginx git curl wget
```

### 3. Criar usuário e diretórios
```bash
useradd -m -s /bin/bash lipsync
mkdir -p /home/lipsync/app
chown -R lipsync:lipsync /home/lipsync
```

### 4. Baixar aplicação
```bash
cd /home/lipsync/app
git clone https://github.com/sterling9879/PARA-VPS.git .
git checkout claude/setup-video-generation-vps-01Gn6naoCU4kVw3UqS1BFHmL
chown -R lipsync:lipsync /home/lipsync/app
```

### 5. Configurar Python
```bash
cd /home/lipsync/app
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-cors python-dotenv requests elevenlabs google-generativeai werkzeug
deactivate
```

### 6. Criar arquivo .env
```bash
cat > /home/lipsync/app/.env << 'EOF'
ELEVENLABS_API_KEY=sua_key_aqui
GEMINI_API_KEY=sua_key_aqui
WAVESPEED_API_KEY=sua_key_aqui
AUTH_EMAIL=admin
AUTH_PASSWORD=SuaSenhaAqui
FLASK_SECRET_KEY=chave_secreta_aleatoria
EOF
chmod 600 /home/lipsync/app/.env
chown lipsync:lipsync /home/lipsync/app/.env
```

### 7. Criar diretórios de trabalho
```bash
mkdir -p /home/lipsync/app/temp/{uploads,outputs,audio}
mkdir -p /home/lipsync/app/data/avatars/thumbnails
mkdir -p /home/lipsync/app/logs
chown -R lipsync:lipsync /home/lipsync/app
```

### 8. Criar serviço systemd
```bash
cat > /etc/systemd/system/lipsync.service << 'EOF'
[Unit]
Description=LipSync Video Generator
After=network.target

[Service]
Type=simple
User=lipsync
Group=lipsync
WorkingDirectory=/home/lipsync/app
Environment="PATH=/home/lipsync/app/venv/bin"
ExecStart=/home/lipsync/app/venv/bin/python web_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable lipsync
systemctl start lipsync
```

### 9. Configurar Nginx
```bash
cat > /etc/nginx/sites-available/lipsync << 'EOF'
server {
    listen 80;
    server_name SEU_DOMINIO www.SEU_DOMINIO;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }
}
EOF

ln -sf /etc/nginx/sites-available/lipsync /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

### 10. Configurar SSL
```bash
certbot --nginx -d SEU_DOMINIO -d www.SEU_DOMINIO
```

## Comandos Úteis

| Comando | Descrição |
|---------|-----------|
| `systemctl status lipsync` | Ver status da aplicação |
| `systemctl restart lipsync` | Reiniciar aplicação |
| `journalctl -u lipsync -f` | Ver logs em tempo real |
| `nano /home/lipsync/app/.env` | Editar configurações |

## Configurar DNS

No painel do seu provedor de domínio, adicione:

| Tipo | Nome | Valor |
|------|------|-------|
| A | @ | IP_DO_SERVIDOR |
| A | www | IP_DO_SERVIDOR |

## Problemas Comuns

### 502 Bad Gateway
```bash
# Verificar se a aplicação está rodando
systemctl status lipsync

# Ver logs de erro
journalctl -u lipsync -n 50

# Reiniciar
systemctl restart lipsync
```

### SSL não funciona
```bash
# Verificar se domínio aponta para o servidor
ping SEU_DOMINIO

# Tentar novamente
certbot --nginx -d SEU_DOMINIO
```

### Permissões
```bash
# Corrigir permissões
chown -R lipsync:lipsync /home/lipsync/app
```

## Suporte

- Logs: `journalctl -u lipsync -f`
- Status: `systemctl status lipsync nginx`
