# 🚀 Guia dos Launchers

## 📋 Visão Geral

Os launchers (`start.bat` e `start.sh`) são scripts automatizados que facilitam a inicialização do LipSync Video Generator Pro. Eles verificam todas as dependências, configuram o ambiente e permitem escolher qual interface usar.

---

## 🖥️ Windows (start.bat)

### Como Usar

1. **Duplo clique** em `start.bat`
2. O script verificará automaticamente:
   - ✅ Se Python está instalado
   - ✅ Se o arquivo `.env` existe
   - ✅ Se as dependências estão instaladas
   - ✅ Se os assets foram criados
3. Escolha a interface desejada no menu

### Opções do Menu

```
[1] 🌟 Interface Profissional (app_pro.py) - RECOMENDADO
    └─ Dashboard, Projetos, Logs em tempo real

[2] 📋 Interface Original (app.py)
    └─ Interface clássica com tabs

[3] 🖥️  Interface GUI Nativa (app_gui.py)
    └─ Aplicação desktop Windows

[4] ⚙️  Executar Setup de Assets
    └─ Recria avatares e templates

[5] ❌ Sair
```

### Verificações Automáticas

#### 1. Python
Se Python não estiver instalado, o script mostrará:
```
❌ ERRO: Python não encontrado!

Por favor, instale Python 3.8+ de: https://www.python.org/downloads/
```

#### 2. Arquivo .env
Se `.env` não existir:
- Cria automaticamente a partir de `.env.example`
- Abre o arquivo no Notepad para edição
- Aguarda você adicionar as API Keys

#### 3. Dependências
Se as dependências não estiverem instaladas:
```
⚠️  Dependências não instaladas!

Deseja instalar agora? (S/N)
```
- Digite `S` para instalar automaticamente
- Digite `N` para cancelar (não poderá continuar)

#### 4. Assets
Se os assets não existirem:
- Executa `setup_assets.py` automaticamente
- Cria avatares, templates e projetos de exemplo

### Cores do Terminal

O script usa cores para melhor visualização:
- 🟢 **Verde** - Sucesso/OK
- 🟡 **Amarelo** - Avisos
- 🔴 **Vermelho** - Erros
- 🔵 **Azul** - Informações

---

## 🐧 Linux/Mac (start.sh)

### Como Usar

1. Abra o terminal
2. Navegue até a pasta do projeto:
   ```bash
   cd /caminho/para/Automation-Ugc
   ```
3. Execute o launcher:
   ```bash
   ./start.sh
   ```

   **Ou**, se ainda não tiver permissão de execução:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

### Opções do Menu

Mesmas opções do Windows:
```
[1] 🌟 Interface Profissional
[2] 📋 Interface Original
[3] 🖥️  Interface GUI Nativa
[4] ⚙️  Executar Setup de Assets
[5] ❌ Sair
```

### Verificações Automáticas

#### 1. Python 3
```bash
[1/5] 🔍 Verificando Python...
```
- Verifica se `python3` está disponível
- Requer Python 3.8 ou superior

#### 2. Arquivo .env
```bash
[2/5] 🔍 Verificando configurações...
```
- Cria `.env` se não existir
- Abre no editor padrão ($EDITOR ou nano)

#### 3. Dependências
```bash
[3/5] 📦 Verificando dependências...
```
- Verifica se Gradio está instalado
- Oferece instalação automática via pip3

#### 4. Assets
```bash
[4/5] 🎭 Verificando assets...
```
- Cria estrutura inicial se necessário

### Cores no Terminal

O script Linux usa códigos ANSI para cores:
- Verde, Amarelo, Vermelho, Azul, Ciano

---

## 🎯 Fluxo de Execução

### Primeira Vez

```
1. Executar launcher
   ↓
2. Python verificado ✓
   ↓
3. .env criado (abre editor)
   ↓
4. Adicionar API Keys manualmente
   ↓
5. Dependências instaladas (S/N)
   ↓
6. Assets criados automaticamente
   ↓
7. Menu de seleção
   ↓
8. Escolher interface
   ↓
9. Aplicação iniciada!
```

### Execuções Subsequentes

```
1. Executar launcher
   ↓
2. Tudo verificado ✓
   ↓
3. Menu de seleção
   ↓
4. Escolher interface
   ↓
5. Aplicação iniciada!
```

---

## 📝 Configuração do .env

Quando o launcher criar o `.env`, edite e adicione suas API Keys:

```bash
# API Keys (OBRIGATÓRIO)
ELEVENLABS_API_KEY=sk_your_key_here
MINIMAX_API_KEY=your_minimax_key_here
GEMINI_API_KEY=AIza_your_key_here
WAVESPEED_API_KEY=your_wavespeed_key_here

# Audio Provider (elevenlabs ou minimax)
AUDIO_PROVIDER=elevenlabs

# Configurações opcionais (pode deixar padrão)
MAX_CONCURRENT_REQUESTS=10
TEMP_FOLDER=./temp
BATCH_SIZE=3
POLL_INTERVAL=10
POLL_TIMEOUT=900
DEFAULT_RESOLUTION=480p
VIDEO_QUALITY=high
```

**Importante:** Pelo menos 1 provedor de áudio deve estar configurado (ElevenLabs OU MiniMax)

---

## ⚙️ Opção 4: Setup de Assets

Quando selecionar esta opção, o script:

1. Executa `python setup_assets.py`
2. Cria/Recria:
   - 📁 Estrutura de diretórios em `projects/`
   - 🎭 6 avatares de exemplo
   - 📝 5 templates pré-configurados
   - 📂 3 projetos de exemplo
3. Retorna ao menu principal

**Use esta opção quando:**
- Quiser resetar os assets
- Deletou a pasta `projects/` acidentalmente
- Quiser começar do zero

---

## 🔄 Retorno ao Menu

Após encerrar uma aplicação:
- **Windows:** Pressione qualquer tecla para voltar ao menu
- **Linux/Mac:** Pressione ENTER para voltar ao menu

Isso permite:
- Trocar de interface rapidamente
- Executar setup novamente
- Não precisar reabrir o launcher

---

## 🐛 Solução de Problemas

### Windows

**Problema:** "Python não encontrado"
```
Solução:
1. Instale Python de: https://www.python.org/downloads/
2. Marque "Add Python to PATH" durante instalação
3. Reinicie o terminal/computador
4. Execute start.bat novamente
```

**Problema:** "Acesso negado" ao executar
```
Solução:
- Clique com botão direito em start.bat
- Selecione "Executar como Administrador"
```

**Problema:** Caracteres estranhos no terminal
```
Solução:
- O script usa UTF-8 (chcp 65001)
- Isso é normal e esperado
- As cores funcionarão corretamente
```

### Linux/Mac

**Problema:** "Permission denied"
```bash
# Solução:
chmod +x start.sh
./start.sh
```

**Problema:** "python3 not found"
```bash
# Ubuntu/Debian:
sudo apt install python3 python3-pip

# Fedora:
sudo dnf install python3 python3-pip

# macOS:
brew install python3
```

**Problema:** Editor não abre
```bash
# Configure seu editor preferido:
export EDITOR=nano    # ou vim, gedit, code, etc.
./start.sh
```

---

## 💡 Dicas

### Atalhos

**Windows:**
- Crie atalho do `start.bat` na área de trabalho
- Altere o ícone para personalizar

**Linux/Mac:**
- Adicione alias no `.bashrc` ou `.zshrc`:
  ```bash
  alias lipsync='cd ~/Automation-Ugc && ./start.sh'
  ```
- Use apenas `lipsync` para iniciar

### Automatização

Para iniciar automaticamente a interface profissional:

**Windows:** Crie `start_auto.bat`:
```batch
@echo off
cd /d "%~dp0"
python app_pro.py
```

**Linux/Mac:** Crie `start_auto.sh`:
```bash
#!/bin/bash
cd "$(dirname "$0")"
python3 app_pro.py
```

---

## 📊 Estrutura de Verificação

```
start.bat / start.sh
│
├─ [1/5] Verificar Python
│   ├─ python --version (Windows)
│   └─ python3 --version (Linux/Mac)
│
├─ [2/5] Verificar .env
│   ├─ Existe? Sim → OK
│   └─ Não? → Criar e abrir editor
│
├─ [3/5] Verificar Dependências
│   ├─ pip list | findstr gradio (Windows)
│   ├─ python3 -c "import gradio" (Linux/Mac)
│   └─ Não instalado? → Oferecer instalação
│
├─ [4/5] Verificar Assets
│   ├─ projects/metadata.json existe?
│   └─ Não? → python setup_assets.py
│
└─ [5/5] Menu de Seleção
    ├─ [1] app_pro.py
    ├─ [2] app.py
    ├─ [3] app_gui.py
    ├─ [4] setup_assets.py
    └─ [5] exit
```

---

## 🎨 Personalização

### Windows: Alterar Cores

Edite `start.bat` e modifique as linhas `color`:
```batch
color 0A  :: Verde sobre preto
color 0B  :: Azul sobre preto
color 0C  :: Vermelho sobre preto
color 0E  :: Amarelo sobre preto
```

Códigos de cor:
- `0` = Preto
- `1` = Azul
- `2` = Verde
- `3` = Ciano
- `4` = Vermelho
- `9` = Azul claro
- `A` = Verde claro
- `C` = Vermelho claro
- `E` = Amarelo claro

### Linux/Mac: Alterar Cores

Edite `start.sh` e modifique as variáveis:
```bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
```

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique se Python 3.8+ está instalado
2. Verifique se o `.env` tem todas as API Keys
3. Tente executar manualmente:
   ```bash
   python app_pro.py
   ```
4. Consulte os logs de erro no terminal

---

## 🔄 Atualização

Para atualizar o launcher:

```bash
# Git pull para obter última versão
git pull origin main

# Ou baixe manualmente:
# - start.bat (Windows)
# - start.sh (Linux/Mac)
```

---

**Desenvolvido com ❤️ - LipSync Video Generator Pro v2.0**
