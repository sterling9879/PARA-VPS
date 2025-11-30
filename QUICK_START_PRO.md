# 🚀 Quick Start - Interface Profissional

## ⚡ Início Rápido (3 minutos)

### 1️⃣ Setup Inicial

```bash
# 1. Instale dependências (se ainda não instalou)
pip install -r requirements.txt

# 2. Configure as API Keys no arquivo .env
cp .env.example .env
nano .env  # Edite e adicione suas keys

# 3. Execute o setup de assets
python setup_assets.py
```

O setup criará:
- ✅ Estrutura de pastas em `projects/`
- ✅ 6 avatares de exemplo
- ✅ 5 templates pré-configurados
- ✅ 3 projetos de exemplo

### 2️⃣ Inicie a Interface

```bash
python app_pro.py
```

Acesse: **http://localhost:7860**

---

## 📊 Visão Geral da Interface

A interface possui **3 abas principais**:

### 1. 📊 Dashboard
- **Métricas**: Vídeos gerados, projetos, avatares, templates
- **Estatísticas**: Tempo total, caracteres processados
- **Histórico**: 5 vídeos mais recentes
- **Botão**: Atualizar estatísticas

### 2. 📁 Projetos
- **Novo Projeto**: Crie projetos para organizar vídeos
- **Meus Projetos**: Liste e gerencie todos os projetos

### 3. 🎬 Gerar Vídeo
- **Seleção de Projeto**: Escolha onde salvar
- **Roteiro**: Digite seu script
- **Provedor**: ElevenLabs ou MiniMax
- **Voz**: Seleção automática por provedor
- **Imagens**: Upload de 1-20 imagens
- **Logs**: Terminal em tempo real
- **Vídeo**: Player integrado

---

## 🎯 Primeiro Vídeo (Passo a Passo)

### Passo 1: Criar um Projeto

1. Vá para **📁 Projetos** → **➕ Novo Projeto**
2. Nome: `Meu Primeiro Projeto`
3. Descrição: `Teste da interface profissional`
4. Clique em **➕ Criar Projeto**

### Passo 2: Preparar Conteúdo

1. Vá para **🎬 Gerar Vídeo**
2. Selecione seu projeto no dropdown
3. Cole este roteiro de teste:

```
Olá! Este é um teste do LipSync Video Generator Pro.

Estou testando a interface profissional com sistema de projetos.

A qualidade do vídeo gerado é impressionante!
```

### Passo 3: Configurar

1. **Provedor**: Escolha ElevenLabs ou MiniMax
2. **Voz**: Aguarde carregar e selecione uma voz
3. **Modelo**: Deixe "Multilingual v3" (ElevenLabs)
4. **Imagens**: Faça upload de 2-3 fotos suas ou de avatares
5. **Vídeos Simultâneos**: Deixe em 3

### Passo 4: Gerar

1. Clique em **🎬 GERAR VÍDEO**
2. Acompanhe os logs em tempo real no terminal
3. Aguarde a conclusão (2-5 minutos)
4. Vídeo aparecerá automaticamente no player

### Passo 5: Verificar

1. Volte para **📊 Dashboard**
2. Clique em **🔄 Atualizar Estatísticas**
3. Veja suas métricas atualizadas!

---

## 🎨 Visual da Interface

### Tema Dark/Tech

A interface usa um esquema de cores tecnológico:

- **Azul Ciano**: `#00d4ff` - Elementos primários
- **Roxo**: `#7b2cbf` - Elementos secundários
- **Verde Neon**: `#06ffa5` - Sucesso/completo
- **Fundo Escuro**: `#0a0e27` - Background principal
- **Cards**: `#1a1f3a` - Elementos de conteúdo

### Elementos Visuais

- ✨ **Gradientes animados** nos botões
- 🎯 **Hover effects** em cards
- 📊 **Barra de progresso** com gradiente
- 💻 **Terminal estilizado** para logs
- 🎨 **Badges coloridos** de status

---

## 📂 Estrutura Criada

Após o setup, você terá:

```
Automation-Ugc/
├── projects/                    # Diretório de projetos
│   ├── avatars/                # Biblioteca de avatares
│   │   ├── male/              # Avatares masculinos
│   │   ├── female/            # Avatares femininos
│   │   └── custom/            # Avatares personalizados
│   ├── templates/             # Templates de vídeo
│   ├── outputs/               # Vídeos gerados
│   │   └── [PROJETOS]/       # Um diretório por projeto
│   └── metadata.json          # Metadados do sistema
├── app_pro.py                 # Interface profissional
├── setup_assets.py            # Script de setup
└── project_manager.py         # Gerenciador de projetos
```

---

## 🔧 Configurações Importantes

### API Keys (.env)

```bash
# Provedores de Áudio (pelo menos 1 obrigatório)
ELEVENLABS_API_KEY=sk_...
MINIMAX_API_KEY=your_key...

# Outras APIs (obrigatórias)
GEMINI_API_KEY=AIza...
WAVESPEED_API_KEY=your_key...

# Provedor padrão
AUDIO_PROVIDER=elevenlabs
```

### Concorrência

- **max_workers (slider)**: Quantos vídeos processar simultaneamente
- **Recomendado**: 3-5 para melhor performance
- **Mais alto**: Mais rápido, mas usa mais créditos
- **Mais baixo**: Mais lento, mas economiza créditos

---

## 💡 Dicas Rápidas

### Para Melhor Performance

1. ✅ Use templates para vídeos recorrentes
2. ✅ Organize em projetos desde o início
3. ✅ Mantenha biblioteca de avatares organizada
4. ✅ Configure max_workers entre 3-5
5. ✅ Prepare roteiros em lote

### Para Economizar Tempo

1. 📝 Crie templates com configurações testadas
2. 🎭 Use avatares da biblioteca
3. 📁 Organize por tipo de conteúdo
4. 🔄 Revise estatísticas regularmente

### Para Melhor Organização

1. 📂 Um projeto por campanha/série
2. 🏷️ Nomes descritivos nos projetos
3. 📋 Descrições detalhadas
4. 🗂️ Categorize avatares corretamente

---

## ❓ Perguntas Frequentes

### Como ver meus vídeos gerados?

**R:** Vá para `projects/outputs/[SEU_PROJETO]/` ou veja no Dashboard os vídeos recentes.

### Posso usar ambos ElevenLabs e MiniMax?

**R:** Sim! Configure ambas as keys e escolha na interface qual usar.

### Os projetos são salvos permanentemente?

**R:** Sim, tudo é salvo em `projects/metadata.json` e persiste entre execuções.

### Posso deletar projetos?

**R:** Atualmente não pela interface. Delete manualmente a pasta e a entrada no JSON.

### Como adicionar mais avatares?

**R:** Copie imagens para `projects/avatars/[categoria]/` e registre no metadata.json

### Os templates são editáveis?

**R:** Sim, edite `projects/metadata.json` manualmente ou recrie via código.

---

## 🆘 Solução de Problemas

### Erro: "Nenhum provedor configurado"

**Solução:**
```bash
# Verifique o arquivo .env
cat .env | grep API_KEY

# Configure pelo menos uma key
nano .env
```

### Interface não carrega

**Solução:**
```bash
# Reinstale dependências
pip install -r requirements.txt --upgrade

# Execute novamente
python app_pro.py
```

### Projeto não aparece

**Solução:**
```bash
# Execute o setup novamente
python setup_assets.py

# Ou crie manualmente
python -c "from project_manager import ProjectManager; pm = ProjectManager(); pm.create_project('Teste', 'Desc')"
```

### Logs não aparecem

**Solução:**
- Verifique o console do terminal
- Recarregue a página (F5)
- Reinicie a aplicação

---

## 📚 Próximos Passos

1. ✅ Explore o Dashboard
2. ✅ Crie seu primeiro projeto
3. ✅ Gere seu primeiro vídeo
4. ✅ Experimente diferentes vozes e provedores
5. ✅ Crie templates personalizados
6. ✅ Organize sua biblioteca de avatares
7. ✅ Leia o guia completo: `INTERFACE_PRO_GUIDE.md`

---

## 🎓 Recursos Adicionais

- **Guia Completo**: `INTERFACE_PRO_GUIDE.md`
- **Documentação API**: Veja arquivos individuais
- **Exemplos**: Templates pré-configurados no setup

---

## 🚀 Comece Agora!

```bash
# 1. Setup
python setup_assets.py

# 2. Inicie
python app_pro.py

# 3. Acesse
# http://localhost:7860

# 4. Divirta-se! 🎉
```

---

**Desenvolvido com ❤️ - LipSync Video Generator Pro v2.0**
