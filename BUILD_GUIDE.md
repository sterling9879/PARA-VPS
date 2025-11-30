# 🔨 Guia Rápido - Build do Executável

## Como criar o arquivo .exe em 3 passos

---

## ⚡ Método Rápido

```batch
# Execute apenas isto:
build_exe.bat
```

**Pronto!** O executável estará em `dist/LipSync_Video_Generator/`

---

## 📋 Pré-requisitos

Antes de executar o build:

- ✅ Python 3.8+ instalado
- ✅ Projeto funcionando (testado com `python app.py`)
- ✅ Todas as dependências instaladas (`pip install -r requirements.txt`)

---

## 🎯 Passo a Passo Detalhado

### 1. Preparação

```batch
# Certifique-se de que o ambiente virtual está ativo
venv\Scripts\activate

# Instale dependências de build (se necessário)
pip install -r requirements-exe.txt
```

### 2. Build

```batch
# Execute o script de build
build_exe.bat
```

**O que o script faz:**
1. Ativa ambiente virtual
2. Instala PyInstaller
3. Limpa builds anteriores
4. Gera executável usando `app.spec`
5. Cria estrutura de distribuição
6. Adiciona arquivos de suporte

**Tempo estimado:** 3-5 minutos

### 3. Teste

```batch
# Entre na pasta do executável
cd dist\LipSync_Video_Generator

# Execute para testar
INICIAR.bat
```

**Verifique:**
- ✅ Interface abre no navegador
- ✅ Vozes carregam corretamente
- ✅ Pode fazer upload de imagens
- ✅ Console mostra logs sem erros

---

## 📦 Arquivos Gerados

```
dist/LipSync_Video_Generator/
├── LipSync_Video_Generator.exe    # ⭐ Executável principal
├── INICIAR.bat                     # Atalho de inicialização
├── README_EXE.txt                  # Instruções para usuário
├── .env.example                    # Template de configuração
└── _internal/                      # Bibliotecas (não mexer)
    ├── gradio/
    ├── elevenlabs/
    ├── google/
    └── ... (300-400 MB)
```

---

## 🚀 Distribuir

### Criar ZIP para distribuição:

```batch
# Comprima a pasta completa
cd dist
7z a -tzip LipSync_Video_Generator_v1.0.zip LipSync_Video_Generator\
```

**Ou use o Windows Explorer:**
1. Clique direito em `LipSync_Video_Generator`
2. Enviar para → Pasta compactada

---

## ⚙️ Customizar Build

### Alterar configurações:

Edite o arquivo `app.spec`:

```python
# Mudar nome do executável
exe = EXE(
    ...
    name='MeuApp',  # Novo nome
    ...
)

# Adicionar ícone
exe = EXE(
    ...
    icon='icon.ico',  # Caminho do ícone
    ...
)

# Remover console (janela preta)
exe = EXE(
    ...
    console=False,  # Interface pura
    ...
)
```

### Rebuild após mudanças:

```batch
pyinstaller app.spec --clean --noconfirm
```

---

## 🐛 Problemas Comuns

### ❌ "PyInstaller não encontrado"

```batch
pip install pyinstaller
```

### ❌ "ModuleNotFoundError no executável"

Adicione o módulo faltante em `app.spec`:

```python
hiddenimports=[
    'modulo_faltante',  # Adicione aqui
    ...
]
```

### ❌ "Executável muito grande (>1GB)"

Optimize excludindo módulos desnecessários em `app.spec`:

```python
excludes=[
    'matplotlib',
    'scipy',
    'pandas',
    ...
]
```

### ❌ "Erro ao executar o .exe"

1. Teste em máquina limpa (sem Python)
2. Verifique console para erros
3. Confirme que FFmpeg está instalado
4. Valide arquivo `.env`

---

## 🎨 Criar Instalador Profissional (Opcional)

### Usar NSIS:

1. **Instale NSIS:**
   - Download: https://nsis.sourceforge.io/Download

2. **Gere o executável primeiro:**
   ```batch
   build_exe.bat
   ```

3. **Compile o instalador:**
   - Clique direito em `installer.nsi`
   - "Compile NSIS Script"

4. **Resultado:**
   - `LipSync_Video_Generator_Setup.exe` (instalador completo)

**Vantagens do instalador:**
- ✅ Cria atalhos automaticamente
- ✅ Adiciona no menu Iniciar
- ✅ Desinstalador integrado
- ✅ Aparência profissional

---

## 📊 Tamanhos de Referência

| Componente | Tamanho |
|-----------|---------|
| Executável base | ~5 MB |
| Gradio | ~50 MB |
| ElevenLabs SDK | ~10 MB |
| Google AI | ~30 MB |
| Outras dependências | ~200 MB |
| **Total (dist/)** | **~300-400 MB** |
| **ZIP compactado** | **~150-200 MB** |

---

## ✅ Checklist Pré-Distribuição

Antes de distribuir o executável:

- [ ] Testado em máquina limpa (sem Python)
- [ ] Testado em Windows 10 e 11
- [ ] README_EXE.txt está claro
- [ ] .env.example não contém chaves reais
- [ ] FFmpeg requirement está documentado
- [ ] Versão está documentada (v1.0, v1.1, etc)
- [ ] Suporte/contato está disponível

---

## 🔄 Atualizar Versão

Para criar uma nova versão:

1. **Atualize o código:**
   ```batch
   git pull origin main
   ```

2. **Teste as mudanças:**
   ```batch
   python app.py
   ```

3. **Rebuilde:**
   ```batch
   build_exe.bat
   ```

4. **Renomeie a distribuição:**
   ```
   LipSync_Video_Generator_v1.0.zip → v1.1.zip
   ```

5. **Documente mudanças:**
   - Atualize CHANGELOG.md
   - Liste o que mudou

---

## 📞 Ajuda

- 📖 **Documentação completa:** `DISTRIBUICAO_EXE.md`
- 🐛 **Troubleshooting:** `TROUBLESHOOTING.md`
- 💬 **Suporte:** Abra issue no GitHub

---

**Boa sorte com seu build!** 🚀
