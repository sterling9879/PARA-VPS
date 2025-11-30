# 🚀 Guia Google Colab - LipSync Video Generator

## Execute o sistema completo no navegador, sem instalar nada!

---

## 🎯 O Que É Este Colab?

Um **notebook Jupyter** pronto para usar que permite gerar vídeos com lip-sync diretamente no **Google Colab**, sem precisar instalar Python, dependências ou configurar ambiente local.

### ✨ Vantagens:

- ✅ **Zero instalação** - Roda no navegador
- ✅ **Gratuito** - Usa recursos do Google Colab
- ✅ **Fácil** - Interface Gradio familiar
- ✅ **Compartilhável** - Link público para outras pessoas usarem
- ✅ **Rápido setup** - 2-3 minutos para começar

---

## 🚀 Como Usar

### **Passo 1: Abrir o Colab**

Clique no link abaixo para abrir diretamente:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sterling9879/Automation-Ugc/blob/main/LipSync_Video_Generator.ipynb)

**Ou:**

1. Acesse: https://colab.research.google.com/
2. Arquivo → Abrir notebook → GitHub
3. Cole: `https://github.com/sterling9879/Automation-Ugc`
4. Selecione: `LipSync_Video_Generator.ipynb`

---

### **Passo 2: Executar as Células**

Execute as células na ordem (Shift + Enter):

#### 1️⃣ **Instalação (3-5 minutos)**
```python
# Célula: Instalação de Dependências
⏯️ Execute
```

Instala:
- FFmpeg
- Gradio
- ElevenLabs SDK
- Google GenerativeAI
- Outras bibliotecas

#### 2️⃣ **Configurar API Keys**
```python
# Célula: Configuração de API Keys
🔑 Cole suas chaves aqui
⏯️ Execute
```

**Onde obter:**
- Gemini: https://ai.google.dev/
- ElevenLabs: https://elevenlabs.io/app/settings
- WaveSpeed: https://wavespeed.ai/

**Duas opções:**

**Opção A - Colar diretamente (mais rápido):**
```python
GEMINI_API_KEY = "AIzaSy..."
ELEVENLABS_API_KEY = "sk_..."
WAVESPEED_API_KEY = "ws_..."
```

**Opção B - Colab Secrets (mais seguro):**
1. Clique no ícone 🔑 na barra lateral
2. Adicione suas secrets
3. Descomente o código no notebook

#### 3️⃣ **Baixar Código**
```python
# Célula: Baixar Código do Projeto
⏯️ Execute
```

Clona o repositório do GitHub.

#### 4️⃣ **Testar APIs (opcional)**
```python
# Célula: Testar Conexões
⏯️ Execute
```

Verifica se todas as APIs estão funcionando.

#### 5️⃣ **Iniciar Interface**
```python
# Célula: Iniciar Interface Gradio
⏯️ Execute
```

Abre interface Gradio com link público!

---

### **Passo 3: Usar a Interface**

Após executar a última célula, você verá:

```
Running on public URL: https://xxxxx.gradio.live
```

**Clique no link!** A interface vai abrir:

1. **📝 Roteiro:** Cole seu texto
2. **🎤 Voz:** Selecione do ElevenLabs
3. **🤖 Modelo:** Escolha (v3 recomendado)
4. **🖼️ Imagens:** Upload 1-20 imagens
5. **🎬 Gerar:** Clique e aguarde!

---

## 📊 Tempo de Processamento

**Exemplo:** Roteiro de 2000 caracteres

| Etapa | Tempo |
|-------|-------|
| Formatação (Gemini) | ~10s |
| Geração de áudios (ElevenLabs) | ~20-30s |
| Geração de vídeos (WaveSpeed) | ~5-8 min |
| Concatenação (FFmpeg) | ~10s |
| **TOTAL** | **~6-9 min** |

**Observação:** Vídeos são processados em **paralelo** pelo WaveSpeed!

---

## 💾 Download dos Vídeos

### **Opção 1: Pela Interface Gradio**
- Clique nos 3 pontinhos no player de vídeo
- Selecione "Download"

### **Opção 2: Pelo Colab**
Execute a célula "Download dos Vídeos":

```python
# Célula: Download dos Vídeos
⏯️ Execute
```

Faz download automático de todos os vídeos gerados.

---

## 🔧 Configurações Avançadas

### Link Público Permanente

Por padrão, o link Gradio expira em **72 horas**.

Para link mais longo, use Gradio Pro ou configure ngrok:

```python
# Instalar ngrok
!pip install pyngrok
from pyngrok import ngrok

# Configurar token
ngrok.set_auth_token("seu_token_aqui")

# Criar túnel
public_url = ngrok.connect(7860)
print(f"🔗 URL permanente: {public_url}")
```

### Aumentar Memória/GPU

Se precisar de mais recursos:

1. **Runtime → Change runtime type**
2. Hardware accelerator: **GPU** ou **TPU**
3. RAM: **High-RAM**

**Observação:** Este projeto não precisa de GPU, mas pode ajudar em casos extremos.

### Alterar Modelo Padrão

Edite no código:

```python
# Em app.py, linha 223
value="eleven_multilingual_v3"  # Mude aqui
```

---

## 🐛 Solução de Problemas

### ❌ Erro: "Module not found"

**Causa:** Instalação incompleta

**Solução:**
```python
# Re-execute célula de instalação
!pip install --upgrade gradio elevenlabs google-generativeai
```

### ❌ Erro: "Invalid API key"

**Causa:** Chave incorreta ou não configurada

**Solução:**
1. Verifique suas chaves em https://ai.google.dev/, https://elevenlabs.io/, https://wavespeed.ai/
2. Re-execute célula de configuração
3. Confirme que não há espaços extras

### ❌ Interface não abre

**Causa:** Link expirou ou Colab desconectou

**Solução:**
1. Verifique se Colab está conectado (canto superior direito)
2. Re-execute célula "Iniciar Interface"
3. Use o novo link gerado

### ❌ Colab desconectou durante processamento

**Causa:** Timeout de inatividade (sessão gratuita)

**Solução:**
- Mantenha aba ativa
- Mova o mouse ocasionalmente
- Ou use Colab Pro (sem timeout)

### ❌ Erro: "Disk quota exceeded"

**Causa:** Muitos arquivos temporários

**Solução:**
```python
# Execute célula de limpeza
!rm -rf temp/
```

### ❌ FFmpeg não encontrado

**Causa:** Instalação falhou

**Solução:**
```python
!apt-get update
!apt-get install -y ffmpeg
!ffmpeg -version  # Verificar
```

---

## 💡 Dicas de Uso

### ✅ Mantenha Colab Ativo

Sessões gratuitas desconectam após inatividade:
- Mova mouse ocasionalmente
- Ou abra console (F12) e execute:
  ```javascript
  function KeepAlive() {
    console.log("Keeping alive...");
  }
  setInterval(KeepAlive, 60000);
  ```

### ✅ Use Imagens de Qualidade

- Alta resolução (mínimo 512x512)
- Boa iluminação
- Fundo limpo
- Rosto centralizado

### ✅ Divida Textos Longos

Se o roteiro for muito longo (>10.000 caracteres):
1. Divida em partes menores
2. Processe separadamente
3. Una os vídeos depois com ferramentas de edição

### ✅ Escolha o Modelo Certo

| Modelo | Quando Usar |
|--------|-------------|
| **Multilingual v3** | Máxima qualidade, conteúdo final |
| **Turbo v3** | Testes rápidos, iterações |
| **Flash v3** | Produção em massa, custo-benefício |

### ✅ Salve Seu Trabalho

Vídeos são perdidos quando sessão expira:
1. Baixe vídeos imediatamente após gerar
2. Ou salve no Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')

   # Copie vídeos para Drive
   !cp temp/*/final_video.mp4 /content/drive/MyDrive/
   ```

---

## 🆚 Colab vs Local

| Característica | Google Colab | Instalação Local |
|---------------|--------------|------------------|
| Setup | 2-3 minutos | 10-20 minutos |
| Instalação | Automática | Manual |
| Requisitos | Navegador | Python, FFmpeg |
| Custo | Grátis* | Grátis |
| Performance | Boa | Depende do PC |
| Timeout | Sim (sessão gratuita) | Não |
| Acesso remoto | Sim (link público) | Configuração extra |
| Armazenamento | 15 GB | Ilimitado (seu HD) |

*APIs têm custos separados

---

## 💰 Custos

### Google Colab
- ✅ **Grátis** - Tier gratuito
- 💰 **Colab Pro** - $9.99/mês (sem timeout, mais memória)
- 💰 **Colab Pro+** - $49.99/mês (ainda mais recursos)

### APIs (cobradas separadamente)
- 💰 **Gemini** - Gratuito até certo limite
- 💰 **ElevenLabs** - A partir de $5/mês
- 💰 **WaveSpeed** - Por crédito/vídeo

**Estimativa por vídeo de 5 minutos:**
- Gemini: ~$0.001
- ElevenLabs: ~$0.10-0.30
- WaveSpeed: ~$0.50-1.00
- **Total: ~$0.60-1.30/vídeo**

---

## 🔒 Segurança e Privacidade

### ✅ Boas Práticas:

1. **Use Colab Secrets** para API keys (não cole diretamente)
2. **Não compartilhe links** do Colab com chaves expostas
3. **Limpe arquivos** após uso (célula de limpeza)
4. **Baixe vídeos** e delete do Colab
5. **Não commite** notebooks com chaves no GitHub

### ⚠️ Avisos:

- Links Gradio são públicos (qualquer um pode acessar)
- Arquivos no Colab são temporários (deletados após sessão)
- Google pode ver arquivos no Colab (política de privacidade)

---

## 📚 Recursos Adicionais

### Documentação Completa:
- [README.md](README.md) - Documentação principal
- [QUICKSTART.md](QUICKSTART.md) - Início rápido local
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solução de problemas
- [GUI_APP_GUIDE.md](GUI_APP_GUIDE.md) - Versão desktop

### Comunidade:
- 💬 [GitHub Discussions](https://github.com/sterling9879/Automation-Ugc/discussions)
- 🐛 [Issues](https://github.com/sterling9879/Automation-Ugc/issues)
- ⭐ [Dar Star no GitHub](https://github.com/sterling9879/Automation-Ugc)

---

## 🎓 Tutoriais em Vídeo

Planejados:
- [ ] Como configurar API keys
- [ ] Primeiro vídeo no Colab
- [ ] Dicas de otimização
- [ ] Casos de uso práticos

---

## 🤝 Contribuindo

Encontrou um bug ou tem uma sugestão?

1. Abra uma [Issue](https://github.com/sterling9879/Automation-Ugc/issues)
2. Ou envie um Pull Request
3. Feedback é sempre bem-vindo!

---

## 📜 Licença

Este projeto é open-source. Verifique LICENSE para detalhes.

---

## 🎉 Pronto para Começar!

**[📓 Abrir no Google Colab →](https://colab.research.google.com/github/sterling9879/Automation-Ugc/blob/main/LipSync_Video_Generator.ipynb)**

---

**Desenvolvido com ❤️ | Gemini + ElevenLabs + WaveSpeed**

*Versão: 1.0 | Última atualização: 2024*
