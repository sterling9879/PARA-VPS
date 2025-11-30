# 🔧 Guia de Solução de Problemas

## ❌ Erro: "Invalid API key" do ElevenLabs

Se você está vendo este erro:
```
ERROR - Erro ao buscar vozes: status_code: 401, body: {'detail': {'status': 'invalid_api_key', 'message': 'Invalid API key'}}
```

### Solução:

#### 1️⃣ Verifique suas API Keys

Execute este comando para verificar todas as suas chaves:
```bash
python check_api_keys.py
```

Este script irá:
- ✅ Testar cada API key
- 🔍 Mostrar quais estão válidas e quais não estão
- 💡 Dar instruções de como obter chaves válidas

#### 2️⃣ Obtenha uma API Key válida do ElevenLabs

**Opção A - Conta Gratuita:**
1. Acesse: https://elevenlabs.io
2. Crie uma conta (Gmail, GitHub, etc)
3. Vá em: **Settings** → **API Keys**
4. Clique em **Create API Key**
5. Copie a chave gerada

**Opção B - Se já tem conta:**
1. Faça login em: https://elevenlabs.io
2. Clique no ícone do seu perfil (canto superior direito)
3. Vá em **Profile** → **API Keys**
4. Copie sua chave existente ou crie uma nova

#### 3️⃣ Configure a chave no arquivo .env

**Windows:**
```cmd
notepad .env
```

**Linux/Mac:**
```bash
nano .env
```

Encontre a linha:
```env
ELEVENLABS_API_KEY=sk_61d52f67ddbeed5bb9f7ee8701a4f145f14e8cc50e8d34fb
```

Substitua pela sua chave real:
```env
ELEVENLABS_API_KEY=sk_sua_chave_real_aqui
```

**IMPORTANTE:** Não use a chave do exemplo! Ela é inválida.

#### 4️⃣ Salve e teste novamente

```bash
python check_api_keys.py
```

Se ver "✅ ElevenLabs API Key VÁLIDA!", está tudo certo!

---

## ❌ Erro: TypeError: File.__init__() got an unexpected keyword argument 'info'

Se você está vendo este erro ao iniciar o app.py:
```
TypeError: File.__init__() got an unexpected keyword argument 'info'
```

### Solução:

Atualize o Gradio para versão 5.0+:

```bash
# Ativa o ambiente virtual primeiro
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Atualiza o Gradio
pip install --upgrade gradio
```

Ou reinstale todas as dependências:
```bash
pip install -r requirements.txt --upgrade
```

---

## ❌ Erro: "Gemini API Key inválida"

### Solução:

1. Acesse: https://ai.google.dev
2. Clique em **Get API Key**
3. Crie um projeto ou selecione um existente
4. Copie a chave gerada (começa com `AIzaSy...`)
5. Cole no arquivo .env:
```env
GEMINI_API_KEY=AIzaSy_sua_chave_aqui
```

---

## ❌ Erro: "WaveSpeed API Key inválida"

### Solução:

1. Acesse: https://wavespeed.ai
2. Faça login
3. Vá em **API Keys** no dashboard
4. Copie ou crie uma nova chave
5. Cole no arquivo .env:
```env
WAVESPEED_API_KEY=sua_chave_aqui
```

---

## 🔍 Como verificar se as API Keys estão corretas

### Método 1: Script Automático (Recomendado)

```bash
python check_api_keys.py
```

Este script testa todas as APIs e mostra o resultado.

### Método 2: Manualmente

**ElevenLabs:**
```bash
curl -H "xi-api-key: SUA_CHAVE_AQUI" https://api.elevenlabs.io/v1/voices
```

Se retornar uma lista de vozes = ✅ Chave válida
Se retornar erro 401 = ❌ Chave inválida

---

## 🌐 Navegador não abre automaticamente

O sistema agora abre o navegador automaticamente, mas se não funcionar:

1. Veja no terminal a mensagem:
```
Running on local URL:  http://127.0.0.1:7860
```

2. Abra seu navegador manualmente e acesse:
```
http://localhost:7860
```

---

## 🔄 Problemas de Instalação

### Python não reconhecido

**Windows:**
1. Reinstale o Python de: https://www.python.org/downloads/
2. Marque a opção "Add Python to PATH"
3. Reinicie o terminal

**Linux/Mac:**
```bash
sudo apt-get install python3  # Ubuntu/Debian
brew install python3          # macOS
```

### FFmpeg não encontrado

**Windows:**
```cmd
choco install ffmpeg
```

Ou baixe de: https://ffmpeg.org/download.html

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### Dependências não instalam

```bash
# Limpa cache e reinstala
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

---

## 📝 Checklist de Diagnóstico

Antes de pedir ajuda, verifique:

- [ ] Python 3.8+ instalado: `python --version`
- [ ] FFmpeg instalado: `ffmpeg -version`
- [ ] Ambiente virtual ativado
- [ ] Arquivo .env existe
- [ ] API keys configuradas no .env
- [ ] API keys validadas com: `python check_api_keys.py`
- [ ] Dependências instaladas: `pip install -r requirements.txt`
- [ ] Porta 7860 livre (nenhum outro app usando)

---

## 🆘 Comandos Úteis

### Verificar tudo

```bash
python test_setup.py
python check_api_keys.py
```

### Reinstalar do zero

**Windows:**
```cmd
rmdir /s /q venv
install.bat
```

**Linux/Mac:**
```bash
rm -rf venv
./install.sh
```

### Ver logs detalhados

```bash
python app.py
```

Os logs aparecerão no terminal.

---

## 💡 Dicas

1. **Sempre ative o ambiente virtual** antes de executar qualquer comando Python
2. **Não compartilhe suas API keys** - elas são secretas
3. **Use contas gratuitas para testar** - todas as APIs oferecem tier gratuito
4. **Verifique os limites** - APIs gratuitas têm limites de uso
5. **Mantenha o terminal aberto** - você verá mensagens de erro úteis

---

## 📞 Links Úteis

- ElevenLabs: https://elevenlabs.io
- Gemini: https://ai.google.dev
- WaveSpeed: https://wavespeed.ai
- Python: https://www.python.org/downloads/
- FFmpeg: https://ffmpeg.org/download.html

---

**Última atualização:** Novembro 2025
