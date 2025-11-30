# 🪟 Guia de Instalação para Windows

## 🚀 Instalação Automática (Recomendado)

### Opção 1: Instalação com 1 Clique

1. **Clique duas vezes em:** `install.bat`

2. **Aguarde a instalação** (pode levar alguns minutos)

3. **Configure suas API Keys** quando solicitado

4. **Pronto!** Execute `start.bat` para iniciar

### Opção 2: Instalação Manual

Se preferir fazer passo a passo:

#### 1️⃣ Instale o Python

- Baixe: https://www.python.org/downloads/
- **IMPORTANTE:** Marque a opção "Add Python to PATH"
- Versão mínima: Python 3.8

#### 2️⃣ Instale o FFmpeg

**Opção A - Via Chocolatey (Mais Fácil):**
```cmd
choco install ffmpeg
```

**Opção B - Manual:**
1. Baixe: https://ffmpeg.org/download.html
2. Extraia em uma pasta (ex: `C:\ffmpeg`)
3. Adicione ao PATH:
   - Painel de Controle → Sistema → Configurações Avançadas
   - Variáveis de Ambiente
   - Path → Editar → Novo
   - Adicione: `C:\ffmpeg\bin`

#### 3️⃣ Execute o Instalador

Clique duas vezes em: **`install.bat`**

O script irá:
- ✅ Verificar Python e FFmpeg
- ✅ Criar ambiente virtual
- ✅ Instalar todas as dependências
- ✅ Criar arquivo .env
- ✅ Executar testes

## 🎮 Como Usar

### Iniciar a Aplicação

**Opção 1:** Clique duas vezes em `start.bat`

**Opção 2:** No terminal:
```cmd
start.bat
```

A interface web abrirá em: **http://localhost:7860**

### Testar a Configuração

```cmd
test.bat
```

## 📁 Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| **install.bat** | Instala tudo automaticamente |
| **start.bat** | Inicia a aplicação |
| **test.bat** | Testa a configuração |

## 🐛 Problemas Comuns no Windows

### "Python não é reconhecido como comando"

**Solução:**
1. Reinstale o Python
2. Marque "Add Python to PATH"
3. Ou adicione manualmente ao PATH:
   - `C:\Users\SeuUsuario\AppData\Local\Programs\Python\Python3X`

### "FFmpeg não encontrado"

**Solução:**
1. Instale via Chocolatey: `choco install ffmpeg`
2. OU baixe e adicione ao PATH manualmente

### "Erro ao criar ambiente virtual"

**Solução:**
```cmd
python -m pip install --upgrade pip
python -m venv venv --clear
```

### Scripts .bat não executam

**Solução:**
1. Clique com botão direito → "Executar como Administrador"
2. Ou abra o terminal como Administrador primeiro

### Erro de permissão ao executar scripts

**Solução:**
```cmd
powershell -ExecutionPolicy Bypass
```

### Antivírus bloqueia a instalação

**Solução:**
- Adicione a pasta do projeto às exceções do antivírus
- Temporariamente desabilite o antivírus durante instalação

## ⚡ Comandos Rápidos

### Limpar e Reinstalar

```cmd
rmdir /s /q venv
del /q temp\*.*
install.bat
```

### Atualizar Dependências

```cmd
venv\Scripts\activate
pip install -r requirements.txt --upgrade
```

### Ver Logs

```cmd
venv\Scripts\activate
python app.py
```

## 📊 Verificar Instalação

Após executar `install.bat`, você deve ver:

```
✅ Python 3.X.X encontrado
✅ FFmpeg X.X encontrado
✅ Ambiente virtual criado
✅ Dependências instaladas com sucesso
✅ Arquivo .env encontrado
🎉 Instalação concluída com sucesso!
```

## 🎯 Estrutura de Pastas no Windows

```
C:\Users\SeuUsuario\Automation-Ugc\
├── install.bat          ← Execute este primeiro
├── start.bat            ← Execute para iniciar
├── test.bat             ← Execute para testar
├── venv\                (criado automaticamente)
├── temp\                (criado automaticamente)
├── .env                 (configure suas API keys)
└── ...
```

## 🔧 Configuração Avançada

### Executar em segundo plano

Crie um atalho de `start.bat` e configure:
- Propriedades → Executar: Minimizado

### Iniciar com Windows

1. Pressione `Win + R`
2. Digite: `shell:startup`
3. Copie o atalho de `start.bat` para esta pasta

### Mudar a porta

Edite `app.py`, linha com `server_port`:
```python
app.launch(server_port=8080)  # Mude para porta desejada
```

## 💡 Dicas para Windows

1. **Use PowerShell ou CMD como Administrador** para evitar problemas de permissão

2. **Desabilite temporariamente o antivírus** durante a primeira instalação

3. **Feche outros programas** que possam usar as portas 7860

4. **Mantenha o terminal aberto** enquanto usa a aplicação

5. **Use Ctrl+C** para parar o servidor, não feche diretamente

## 🆘 Suporte

Se encontrar problemas:

1. Execute `test.bat` e veja os erros
2. Verifique se Python e FFmpeg estão no PATH
3. Tente reinstalar com `install.bat`
4. Consulte os logs na pasta `temp\`

## 📞 Links Úteis

- Python Windows: https://www.python.org/downloads/windows/
- FFmpeg Windows: https://www.gyan.dev/ffmpeg/builds/
- Chocolatey: https://chocolatey.org/install
- Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe

---

**Desenvolvido para Windows 10/11** 🪟

Testado em:
- Windows 10 (64-bit)
- Windows 11 (64-bit)
- Python 3.8, 3.9, 3.10, 3.11
