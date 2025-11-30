# 🚀 Guia de Início Rápido

## Instalação em 5 Passos

### 1️⃣ Instale o FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Baixe de: https://ffmpeg.org/download.html
- Adicione ao PATH do sistema

### 2️⃣ Crie e Ative o Ambiente Virtual

```bash
# Cria ambiente virtual
python3 -m venv venv

# Ativa (Linux/macOS)
source venv/bin/activate

# Ativa (Windows)
venv\Scripts\activate
```

### 3️⃣ Instale as Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4️⃣ Configure as API Keys

O arquivo `.env` já está criado com as chaves fornecidas. Se precisar alterar:

```bash
nano .env  # ou use seu editor preferido
```

Certifique-se de que estas linhas estão preenchidas:
```env
ELEVENLABS_API_KEY=sua_chave_aqui
GEMINI_API_KEY=sua_chave_aqui
WAVESPEED_API_KEY=sua_chave_aqui
```

### 5️⃣ Teste a Configuração

```bash
python test_setup.py
```

Se todos os testes passarem ✅, você está pronto!

## 🎬 Iniciar a Aplicação

```bash
python app.py
```

A interface web abrirá em: **http://localhost:7860**

## 📝 Uso Rápido

1. **Digite seu roteiro** no campo de texto
2. **Selecione uma voz** do ElevenLabs
3. **Faça upload de 1-20 imagens** do apresentador
4. **Clique em "Gerar Vídeo"**
5. **Aguarde o processamento** (5-10 minutos típico)
6. **Baixe o vídeo final**

## 🧪 Testar Módulos Individualmente

### Teste o Text Processor:
```bash
python text_processor.py
```

### Teste o Audio Generator:
```bash
python audio_generator.py
```

### Teste o Video Concatenator:
```bash
python video_concatenator.py
```

### Teste o Job Manager:
```bash
python job_manager.py
```

## 📂 Estrutura de Saída

Cada job cria uma pasta:
```
temp/job_{uuid}/
├── formatted_text/
│   ├── batch_1.txt
│   └── ...
├── audios/
│   ├── audio_1.mp3
│   └── ...
├── videos/
│   ├── video_1.mp4
│   └── ...
├── images/
│   └── ...
├── final_output.mp4  ← SEU VÍDEO FINAL
└── state.json
```

## 🐛 Problemas Comuns

### "FFmpeg não encontrado"
- Instale o FFmpeg conforme Passo 1

### "API key inválida"
- Verifique o arquivo `.env`
- Confirme que as chaves estão ativas nas respectivas plataformas

### "Rate limit atingido"
- Aguarde alguns minutos
- Reduza `MAX_CONCURRENT_REQUESTS` em `.env`

### Imports falhando
- Certifique-se de que o ambiente virtual está ativado
- Execute `pip install -r requirements.txt` novamente

## 💡 Dicas

1. **Textos longos:** Divida em seções menores para melhor controle
2. **Imagens:** Use imagens de alta qualidade e bem iluminadas
3. **Vozes:** Teste diferentes vozes para encontrar a ideal
4. **Custos:** Use o botão "Estimar" antes de processar

## 📚 Documentação Completa

Veja `README.md` para documentação detalhada.

## 🎯 Próximos Passos

Após a primeira geração bem-sucedida:

1. Personalize o prompt do Gemini em `text_processor.py`
2. Ajuste as configurações em `.env`
3. Explore diferentes vozes e estilos
4. Experimente com diferentes tipos de imagens

---

**Dúvidas?** Consulte `README.md` ou abra uma issue no GitHub!
