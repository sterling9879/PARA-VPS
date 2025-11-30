# 📦 Guia de Distribuição - Executável Windows

## Gerador de Vídeos com Lip-Sync - Versão Executável

---

## 🎯 Visão Geral

Este guia explica como **criar** e **distribuir** a versão executável do sistema para usuários que **não têm Python instalado**.

---

## 🔨 Como Criar o Executável

### Pré-requisitos para Build:

1. ✅ Windows 10/11
2. ✅ Python 3.8+ instalado
3. ✅ Projeto já configurado e funcionando
4. ✅ Todas as dependências instaladas

### Passo a Passo:

#### **Opção 1: Build Automático (Recomendado)**

```batch
# Execute o script de build
build_exe.bat
```

O script vai:
- ✅ Instalar PyInstaller automaticamente
- ✅ Limpar builds anteriores
- ✅ Gerar o executável
- ✅ Criar estrutura de distribuição
- ✅ Adicionar arquivos de suporte

**Tempo estimado:** 3-5 minutos

#### **Opção 2: Build Manual**

```batch
# Ative o ambiente virtual
venv\Scripts\activate

# Instale PyInstaller
pip install pyinstaller

# Gere o executável
pyinstaller app.spec --clean --noconfirm
```

---

## 📁 Estrutura da Distribuição

Após o build, você terá:

```
dist/LipSync_Video_Generator/
├── LipSync_Video_Generator.exe    # Executável principal
├── INICIAR.bat                     # Atalho para iniciar
├── README_EXE.txt                  # Instruções de uso
├── .env.example                    # Template de configuração
├── _internal/                      # Dependências (não mexer)
│   ├── gradio/
│   ├── elevenlabs/
│   ├── google/
│   └── ... (outras bibliotecas)
└── temp/                           # Criada automaticamente
```

**Tamanho estimado:** 300-500 MB (devido às dependências de IA)

---

## 📤 Como Distribuir

### Método 1: ZIP Simples

1. **Compacte a pasta completa:**
   ```
   dist/LipSync_Video_Generator/ → LipSync_Video_Generator_v1.0.zip
   ```

2. **Distribua o arquivo ZIP via:**
   - Google Drive / Dropbox
   - GitHub Releases
   - Site próprio
   - Email (se o tamanho permitir)

3. **Instruções para o usuário final:**
   - Extrair o ZIP
   - Configurar `.env` com API keys
   - Instalar FFmpeg
   - Executar `INICIAR.bat`

### Método 2: Instalador NSIS (Avançado)

Para criar um instalador profissional `.exe`:

1. **Baixe NSIS:**
   - https://nsis.sourceforge.io/Download

2. **Crie script NSIS:**
   - Exemplo em `installer.nsi` (criar separadamente)

3. **Compile o instalador:**
   - Clique direito no `.nsi` → Compile NSIS Script

---

## 📋 Instruções para o Usuário Final

### 🚀 INÍCIO RÁPIDO (para quem recebe o ZIP)

#### 1. Extrair o Arquivo

```
LipSync_Video_Generator_v1.0.zip
  → Extrair para: C:\LipSync_Video_Generator\
```

#### 2. Instalar FFmpeg

**Windows:**

1. Baixe: https://ffmpeg.org/download.html (Windows builds by BtbN)
2. Extraia para `C:\ffmpeg`
3. Adicione ao PATH:
   - Painel de Controle → Sistema → Configurações Avançadas
   - Variáveis de Ambiente
   - Edite "Path"
   - Adicione: `C:\ffmpeg\bin`

**Verificar instalação:**
```batch
ffmpeg -version
```

#### 3. Configurar API Keys

1. Abra a pasta do programa
2. Renomeie `.env.example` → `.env`
3. Abra `.env` com Bloco de Notas
4. Adicione suas chaves:

```env
GEMINI_API_KEY=sua_chave_do_gemini_aqui
ELEVENLABS_API_KEY=sua_chave_do_elevenlabs_aqui
WAVESPEED_API_KEY=sua_chave_do_wavespeed_aqui
```

**Onde obter as chaves:**
- 🔑 Gemini: https://ai.google.dev/
- 🔑 ElevenLabs: https://elevenlabs.io/app/settings
- 🔑 WaveSpeed: https://wavespeed.ai/

#### 4. Executar o Programa

**Opção A - Atalho (Recomendado):**
```
Duplo clique em: INICIAR.bat
```

**Opção B - Direto:**
```
Duplo clique em: LipSync_Video_Generator.exe
```

**O que vai acontecer:**
- ✅ Console vai abrir mostrando logs
- ✅ Navegador abre automaticamente em `http://localhost:7860`
- ✅ Interface Gradio estará pronta para uso

**⚠️ IMPORTANTE:** Mantenha a janela do console aberta enquanto usa o programa!

#### 5. Usar a Interface

1. **Cole seu roteiro** no campo de texto
2. **Selecione a voz** da lista do ElevenLabs
3. **Escolha o modelo** (Multilingual v2 recomendado)
4. **Faça upload** de 1-20 imagens do apresentador
5. **Clique em "Gerar Vídeo"**
6. **Aguarde** o processamento (progresso mostrado em tempo real)
7. **Baixe** o vídeo final quando concluído

---

## ⚙️ Configurações Avançadas

### Alterar Porta do Servidor

Edite o arquivo `app.py` (necessário rebuild):

```python
app.launch(
    server_name="0.0.0.0",
    server_port=7860,  # Altere aqui
    inbrowser=True
)
```

### Limitar Recursos

No arquivo `config.py`:

```python
MAX_CONCURRENT_REQUESTS = 3  # Reduzir para economizar memória
BATCH_SIZE = 2               # Reduzir para textos menores
```

---

## 🐛 Solução de Problemas (Usuário Final)

### ❌ "FFmpeg não encontrado"

**Solução:**
1. Verifique se FFmpeg está instalado: `ffmpeg -version`
2. Se não estiver, siga as instruções da seção "Instalar FFmpeg"
3. Certifique-se de que está no PATH do sistema

### ❌ "Erro de API Key Inválida"

**Solução:**
1. Verifique se o arquivo `.env` existe (não `.env.example`)
2. Abra `.env` e confirme que as chaves estão corretas
3. Não deixe espaços antes ou depois do `=`
4. Execute `check_api_keys.py` para validar

### ❌ "Porta 7860 em uso"

**Solução:**
1. Feche outros programas que possam usar essa porta
2. Ou altere a porta (veja Configurações Avançadas)

### ❌ Interface não abre no navegador

**Solução:**
1. Abra manualmente: `http://localhost:7860`
2. Verifique o console para erros
3. Confirme que o firewall não está bloqueando

---

## 📊 Comparação: EXE vs Python

| Característica | Versão Python | Versão EXE |
|---------------|---------------|------------|
| Requer Python instalado | ✅ Sim | ❌ Não |
| Tamanho do download | ~50 MB | ~400 MB |
| Velocidade de inicialização | Rápida | Moderada |
| Facilidade de distribuição | Média | Alta |
| Atualizações | Fácil (git pull) | Requer rebuild |
| Customização | Total | Limitada |
| Uso recomendado | Desenvolvedores | Usuários finais |

---

## 🔒 Segurança e Privacidade

### Para Distribuidores:

⚠️ **NUNCA inclua suas API keys no executável!**
- Sempre distribua com `.env.example` vazio
- Instrua usuários a configurar suas próprias chaves

### Para Usuários:

🔐 **Proteja suas API keys:**
- Nunca compartilhe o arquivo `.env`
- Não faça upload dele para Git/nuvem
- Mantenha as chaves seguras

---

## 📝 Checklist de Distribuição

Antes de distribuir, verifique:

- [ ] Executável foi testado em máquina limpa (sem Python)
- [ ] README_EXE.txt está incluído com instruções claras
- [ ] `.env.example` está vazio (sem chaves reais)
- [ ] Documentação menciona necessidade do FFmpeg
- [ ] Versão está documentada (v1.0, v1.1, etc)
- [ ] Changelog está atualizado
- [ ] Licença de uso está clara
- [ ] Forma de contato/suporte está disponível

---

## 🎓 Dicas para Melhorar a Distribuição

### 1. Crie um Ícone Personalizado

Substitua o ícone padrão:

```python
# No arquivo app.spec
exe = EXE(
    ...
    icon='icon.ico',  # Adicione seu ícone aqui
)
```

### 2. Adicione Splash Screen

Use `pyi-splash` para mostrar logo durante inicialização:

```python
# No app.py
import pyi_splash

# ... código de inicialização ...

pyi_splash.close()  # Fecha splash quando pronto
```

### 3. Crie Documentação em Vídeo

Grave um vídeo tutorial mostrando:
- Instalação do FFmpeg
- Configuração do .env
- Primeiro uso
- Exemplos práticos

### 4. Ofereça Suporte

Configure:
- Email de suporte
- FAQ no README
- Issues no GitHub
- Discord/Telegram para comunidade

---

## 🚀 Próximos Passos

Após distribuir com sucesso:

1. **Colete Feedback**
   - Quais erros mais comuns?
   - Onde os usuários travam?
   - O que está confuso?

2. **Crie Updates**
   - Corrija bugs reportados
   - Adicione features solicitadas
   - Melhore documentação

3. **Versione Adequadamente**
   - Use Semantic Versioning (v1.0.0, v1.1.0, v2.0.0)
   - Documente mudanças no CHANGELOG.md
   - Mantenha builds antigos disponíveis

4. **Automatize**
   - Configure CI/CD para builds automáticos
   - Use GitHub Actions para releases
   - Distribua via GitHub Releases

---

## 📞 Suporte

Para problemas com a **criação do executável**, consulte:
- Documentação PyInstaller: https://pyinstaller.org/
- Issues deste projeto no GitHub

Para problemas com o **uso do executável**, consulte:
- README_EXE.txt (incluído no pacote)
- TROUBLESHOOTING.md
- Suporte oficial do projeto

---

**Versão deste guia:** 1.0
**Última atualização:** 2024
**Compatibilidade:** Windows 10/11 (64-bit)
