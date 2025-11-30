# 🎯 Escolha Sua Versão

O LipSync Video Generator possui **duas interfaces disponíveis**. Escolha a que melhor atende suas necessidades:

---

## 🌐 Versão WEB (Gradio)

### Interface web moderna que roda no navegador

**Arquivo principal:** `app.py`

**Vantagens:**
- ✅ Interface web bonita e moderna
- ✅ Acesso remoto possível (compartilhar link)
- ✅ Fácil de usar em qualquer navegador
- ✅ Ideal para servidores e uso remoto
- ✅ Atualização fácil (git pull)

**Desvantagens:**
- ❌ Abre navegador (requer browser)
- ❌ Console visível (janela preta)
- ❌ Maior tamanho (~400 MB)
- ❌ Depende de servidor web interno

### Como usar:

```batch
# Instalar
pip install -r requirements.txt

# Executar
python app.py
# ou
start.bat

# Acessa em: http://localhost:7860
```

### Build para .exe:

```batch
build_exe.bat
```

**Resultado:** Executável que abre navegador

---

## 🖥️ Versão GUI NATIVA (PyQt5)

### Aplicação desktop profissional do Windows

**Arquivo principal:** `app_gui.py`

**Vantagens:**
- ✅ **Interface gráfica NATIVA do Windows**
- ✅ **SEM console** (janela limpa)
- ✅ **Mais leve** (~200-300 MB)
- ✅ **Inicialização mais rápida**
- ✅ **Aparência profissional** (desktop real)
- ✅ **Não requer navegador**
- ✅ Diálogos nativos do Windows
- ✅ Ideal para usuário final

**Desvantagens:**
- ❌ Apenas local (não compartilhável)
- ❌ Requer rebuild para atualizar

### Como usar:

```batch
# Instalar
pip install -r requirements-gui.txt

# Executar
python app_gui.py
```

### Build para .exe NATIVO:

```batch
build_gui.bat
```

**Resultado:** Programa Windows real (sem console!)

---

## 🆚 Comparação Rápida

| Característica | Web (Gradio) | GUI (PyQt5) |
|---------------|--------------|-------------|
| **Interface** | Navegador | Janela Windows nativa |
| **Console** | ✓ Visível | ✗ Oculto |
| **Tamanho** | ~400 MB | ~200-300 MB |
| **Acesso remoto** | ✓ Possível | ✗ Apenas local |
| **Aparência** | Web moderna | Desktop profissional |
| **Inicialização** | Abre navegador | Abre direto |
| **Melhor para** | Servidores/Web | Desktop pessoal |
| **Atualização** | Fácil (git pull) | Requer rebuild |

---

## 🎯 Qual Escolher?

### Escolha **VERSÃO WEB** se você:

- 🌐 Quer acessar remotamente
- 🌐 Prefere interface web
- 🌐 Vai hospedar em servidor
- 🌐 Quer compartilhar com outros
- 🌐 Precisa de atualizações frequentes

### Escolha **VERSÃO GUI** se você:

- 🖥️ Quer programa Windows REAL
- 🖥️ Prefere interface desktop nativa
- 🖥️ Não quer console/janela preta
- 🖥️ Vai usar apenas localmente
- 🖥️ Quer aparência profissional
- 🖥️ Vai distribuir para usuários finais

---

## 📦 Ambas Versões Possuem:

- ✅ Todas as mesmas funcionalidades
- ✅ Processamento paralelo de vídeos
- ✅ Seleção de modelos ElevenLabs
- ✅ Upload múltiplo de imagens
- ✅ Progresso em tempo real
- ✅ Integração com Gemini, ElevenLabs, WaveSpeed
- ✅ Mesmo backend (job_manager)

**A diferença está APENAS na interface!**

---

## 🚀 Recomendação

### Para Desenvolvedores / Uso Pessoal:
👉 **VERSÃO WEB** - Mais flexível, fácil de atualizar

### Para Distribuição / Usuários Finais:
👉 **VERSÃO GUI** - Mais profissional, sem dependências visíveis

### Melhor de Ambos:
👉 **Mantenha as duas!** Use a web para desenvolvimento e a GUI para distribuição

---

## 📚 Documentação

### Versão Web:
- `README.md` - Documentação principal
- `QUICKSTART.md` - Início rápido
- `BUILD_GUIDE.md` - Como criar executável
- `DISTRIBUICAO_EXE.md` - Distribuição

### Versão GUI:
- `GUI_APP_GUIDE.md` - Guia completo da GUI
- `README_GUI.txt` - Para usuário final (gerado no build)

---

## 🔄 Trocar de Versão

Ambas coexistem pacificamente! Você pode:

```batch
# Testar versão web
python app.py

# Testar versão GUI
python app_gui.py

# Buildar ambas
build_exe.bat      # Web com console
build_gui.bat      # GUI sem console
```

---

## 💡 Casos de Uso

### Versão Web é ideal para:
- 🎓 Demonstrações e tutoriais
- 🎓 Testes e desenvolvimento
- 🎓 Compartilhamento temporário (ngrok)
- 🎓 Uso em servidores

### Versão GUI é ideal para:
- 💼 Venda como produto
- 💼 Distribuição comercial
- 💼 Clientes não-técnicos
- 💼 Uso profissional desktop

---

**Escolha a versão que melhor se adapta ao seu caso de uso!**

Ambas são mantidas e funcionam perfeitamente. 🚀
