# 🖥️ Aplicação GUI Nativa do Windows

## Interface Gráfica Profissional com PyQt5

---

## 🎯 Visão Geral

Esta é a **versão desktop nativa** do LipSync Video Generator. Diferente da versão web (Gradio), esta aplicação roda como um **programa Windows real** com interface gráfica PyQt5.

### ✨ Características

- ✅ **Interface gráfica nativa** do Windows (PyQt5)
- ✅ **Sem console** (sem janela preta)
- ✅ **Design moderno** e profissional
- ✅ **Processamento em background** (não trava a interface)
- ✅ **Barra de progresso** em tempo real
- ✅ **Logs visuais** de cada etapa
- ✅ **Não requer navegador** - aplicação standalone
- ✅ **Totalmente autônomo** - não precisa de Python instalado (após build)

---

## 🆚 Comparação: Web vs GUI

| Característica | Versão Web (Gradio) | Versão GUI (PyQt5) |
|---------------|---------------------|-------------------|
| Interface | Navegador web | Janela nativa Windows |
| Console | Visível (logs) | Oculto (interface limpa) |
| Inicialização | Abre navegador | Abre direto |
| Aparência | Web moderna | Desktop profissional |
| Progresso | Gradio progress | QProgressBar nativa |
| Arquivos | Upload web | Seletor de arquivos nativo |
| Tamanho | ~400 MB | ~200-300 MB |
| Dependências | Gradio + FastAPI | PyQt5 |
| Melhor para | Uso remoto/servidor | Desktop pessoal |

---

## 🚀 Como Usar

### Opção 1: Executar com Python

```batch
# Instale dependências
pip install -r requirements-gui.txt

# Execute a aplicação
python app_gui.py
```

### Opção 2: Executável (Recomendado para Distribuição)

```batch
# Gere o executável
build_gui.bat

# Execute o .exe gerado
cd dist\LipSyncVideoGenerator
LipSyncVideoGenerator.exe
```

---

## 🎨 Interface da Aplicação

### Layout Dividido (Splitter)

```
┌─────────────────────────────────────────────────────────┐
│  LipSync Video Generator - Profissional           ─ □ × │
├─────────────────────┬───────────────────────────────────┤
│                     │                                   │
│  PAINEL ESQUERDO   │       PAINEL DIREITO              │
│  (Inputs)          │       (Progresso/Resultado)       │
│                     │                                   │
│  📝 Roteiro         │  ⚙️ Progresso                     │
│  ┌───────────────┐ │  ┌─────────────────────────────┐ │
│  │               │ │  │ Status: Aguardando...       │ │
│  │  [Texto]      │ │  │ [■■■■■░░░░░] 50%            │ │
│  │               │ │  └─────────────────────────────┘ │
│  └───────────────┘ │                                   │
│                     │  📋 Logs                          │
│  🎤 Voz/Modelo     │  ┌─────────────────────────────┐ │
│  [Dropdown ▼]      │  │ [Logs em tempo real...]     │ │
│  [Dropdown ▼]      │  └─────────────────────────────┘ │
│                     │                                   │
│  🖼️ Imagens        │  ✅ Resultado                     │
│  [Lista]           │  [Caminho do vídeo]               │
│  [Botão +]         │  [Abrir Vídeo] [Abrir Pasta]      │
│                     │                                   │
│  [📊 Estimar]      │                                   │
│  [🎬 GERAR VÍDEO]  │                                   │
│                     │                                   │
└─────────────────────┴───────────────────────────────────┘
│ Status: Pronto para gerar vídeos                       │
└─────────────────────────────────────────────────────────┘
```

### Painel Esquerdo - Inputs

1. **📝 Roteiro do Vídeo**
   - Caixa de texto multilinhas
   - Placeholder com instruções
   - Altura mínima: 200px

2. **🎤 Configurações de Voz**
   - Dropdown com vozes do ElevenLabs
   - Dropdown com modelos (multilingual_v2, turbo, etc)

3. **🖼️ Imagens do Apresentador**
   - Botão "Adicionar Imagens"
   - Lista de imagens selecionadas
   - Botão "Remover Selecionadas"

4. **Botões de Ação**
   - 📊 Estimar Custo (azul)
   - 🎬 GERAR VÍDEO (verde, grande)

### Painel Direito - Progresso/Resultado

1. **⚙️ Progresso do Processamento**
   - Label de status (mensagem atual)
   - Barra de progresso (0-100%)

2. **📋 Logs do Sistema**
   - Área de texto read-only
   - Auto-scroll
   - Botão "Limpar Logs"

3. **✅ Vídeo Final**
   - Label com caminho do vídeo
   - Botão "Abrir Vídeo" (abre no player padrão)
   - Botão "Abrir Pasta" (abre no Explorer)

---

## 🛠️ Funcionalidades

### 1. Carregamento de Vozes

Ao abrir, a aplicação:
- Conecta ao ElevenLabs automaticamente
- Lista todas as vozes disponíveis
- Mostra mensagem de erro se falhar

### 2. Seleção de Imagens

Diálogo nativo do Windows:
- Filtro automático: PNG, JPG, JPEG
- Seleção múltipla
- Preview dos nomes na lista

### 3. Estimativa de Custo

Modal com informações:
- Número de caracteres
- Batches a processar
- Vídeos a gerar
- Tempo estimado
- Custo por API (Gemini, ElevenLabs, WaveSpeed)

### 4. Geração de Vídeo

**Validações:**
- Roteiro não vazio
- Pelo menos 1 imagem
- Voz válida selecionada

**Confirmação:**
- Modal perguntando se quer continuar
- Mostra resumo do que será processado

**Processamento:**
- Thread separada (não trava interface)
- Progresso em tempo real
- Logs detalhados
- Botão desabilitado durante processamento

**Conclusão:**
- Modal de sucesso ou erro
- Botões para abrir vídeo/pasta habilitados
- Caminho do vídeo mostrado

---

## 🧵 Arquitetura Técnica

### WorkerThread (QThread)

```python
class WorkerThread(QThread):
    """Thread para processar vídeo sem travar a interface"""
    progress = pyqtSignal(str, int)  # Sinaliza progresso
    finished = pyqtSignal(str, bool) # Sinaliza conclusão
    error = pyqtSignal(str)           # Sinaliza erro
```

**Benefícios:**
- Interface permanece responsiva
- Usuário pode ver logs em tempo real
- Pode cancelar (futuro: adicionar botão cancelar)

### Sinais e Slots (PyQt5)

```python
# Conecta sinais aos slots
self.worker.progress.connect(self.update_progress)
self.worker.finished.connect(self.on_finished)
self.worker.error.connect(self.on_error)
```

**Fluxo:**
1. Thread emite `progress` → UI atualiza barra
2. Thread emite `finished` → UI mostra resultado
3. Thread emite `error` → UI mostra erro

---

## 🎨 Design e Estilo

### Tema: Fusion (PyQt5)

```python
app.setStyle('Fusion')  # Estilo moderno
```

### Cores e Fontes

```css
/* Cores principais */
Background: #f5f5f5 (cinza claro)
GroupBoxes: #ffffff (branco)
Botões: #0078d4 (azul Windows)
Botão Gerar: #107c10 (verde)
Botão Remover: #d13438 (vermelho)

/* Fonte */
Segoe UI, 10pt (padrão Windows)
```

### Componentes Estilizados

- **GroupBox**: Bordas arredondadas, título destacado
- **QPushButton**: Sem bordas, cantos arredondados, hover effect
- **QProgressBar**: Chunk azul, background cinza
- **QTextEdit/QComboBox**: Bordas suaves, padding

---

## 📦 Build do Executável

### Processo Automatizado

```batch
build_gui.bat
```

**O que faz:**
1. Ativa ambiente virtual
2. Instala PyQt5 e PyInstaller
3. Limpa builds anteriores
4. Executa `pyinstaller app_gui.spec`
5. Cria README_GUI.txt
6. Verifica sucesso

### Configuração do Build (app_gui.spec)

```python
exe = EXE(
    ...
    name='LipSyncVideoGenerator',
    console=False,  # ⭐ SEM CONSOLE
    ...
)
```

**Exclusões (reduz tamanho):**
- gradio, fastapi, uvicorn (não usados)
- matplotlib, scipy, pandas (pesados)
- tkinter (interface alternativa)

**Tamanho final:** ~200-300 MB

---

## 🚀 Distribuição

### Criar Pacote ZIP

```batch
cd dist
7z a -tzip LipSyncVideoGenerator_GUI_v1.0.zip LipSyncVideoGenerator\
```

### Conteúdo do Pacote

```
LipSyncVideoGenerator/
├── LipSyncVideoGenerator.exe    # Executável principal
├── README_GUI.txt                # Instruções
├── .env.example                  # Template config
└── _internal/                    # Bibliotecas PyQt5, etc
```

### Instruções para Usuário

1. Extrair ZIP
2. Configurar `.env` com API keys
3. Instalar FFmpeg
4. Executar `LipSyncVideoGenerator.exe`

**Não precisa:**
- Python
- pip
- Ambiente virtual
- Terminal/console

---

## 🐛 Troubleshooting

### Aplicação não abre

**Causa:** Antivírus bloqueando
**Solução:** Adicionar exceção ou executar como Admin

### Erro: "Failed to execute script"

**Causa:** Dependências faltando no build
**Solução:** Adicionar módulo em `hiddenimports` no `.spec`

### Interface travando

**Causa:** Processamento na thread principal
**Solução:** Verificar se `WorkerThread` está sendo usado

### Botões não respondem

**Causa:** Sinais não conectados
**Solução:** Verificar `.connect()` dos botões

---

## 🔧 Customizações

### Adicionar Ícone

```python
# No app_gui.py
self.setWindowIcon(QIcon('icon.ico'))

# No app_gui.spec
exe = EXE(
    ...
    icon='icon.ico',
)
```

### Mudar Cores

Edite a stylesheet em `init_ui()`:

```python
self.setStyleSheet("""
    QPushButton {
        background-color: #YOUR_COLOR;
    }
""")
```

### Adicionar Botão Cancelar

```python
# No app_gui.py
cancel_btn = QPushButton("❌ Cancelar")
cancel_btn.clicked.connect(self.cancel_processing)

def cancel_processing(self):
    if self.worker and self.worker.isRunning():
        self.worker.terminate()
        self.log("⚠️ Processamento cancelado")
```

### Adicionar Preview de Imagens

```python
# Ao selecionar imagem
pixmap = QPixmap(image_path)
label = QLabel()
label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
```

---

## 📊 Performance

### Tempo de Inicialização

- Python: ~2-3 segundos
- Executável: ~5-8 segundos (primeira vez)

### Uso de Memória

- Idle: ~150 MB
- Processando: ~300-500 MB

### Responsividade

- Interface permanece responsiva durante todo o processamento
- Progresso atualiza a cada 100-500ms

---

## 🎓 Próximos Passos

### Melhorias Sugeridas

1. **Preview de vídeo integrado**
   - Usar QMediaPlayer para preview
   - Mostrar vídeo na própria interface

2. **Histórico de jobs**
   - Salvar jobs anteriores
   - Re-processar com um clique

3. **Editor de roteiro integrado**
   - Syntax highlighting
   - Contador de caracteres
   - Divisão de batches visual

4. **Configurações avançadas**
   - Janela de settings
   - Customizar batch size
   - Escolher pasta de output

5. **Arrastar e soltar**
   - Drag & drop de imagens
   - Drag & drop de arquivo de texto

6. **Multi-idioma**
   - Interface em PT/EN/ES
   - QTranslator

---

## 📝 Conclusão

A versão GUI é ideal para:

✅ **Usuários finais** que querem uma aplicação desktop
✅ **Distribuição comercial** (aparência profissional)
✅ **Offline/local** (não precisa de servidor)
✅ **Windows nativamente** (não requer navegador)

**Comparada à versão web:**
- Mais rápida de iniciar
- Mais leve (sem Gradio/FastAPI)
- Mais profissional (interface nativa)
- Melhor integração com Windows

---

**Versão:** 1.0
**Compatibilidade:** Windows 10/11 (64-bit)
**Framework:** PyQt5 5.15+
