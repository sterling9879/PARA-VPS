# 🎬 Roteiro de Narração - Vídeo Tutorial de Instalação

## Sistema de Geração de Vídeos com Lip-Sync

---

## 📋 Informações do Vídeo

**Duração estimada:** 8-10 minutos
**Tom:** Profissional, didático e amigável
**Público-alvo:** Desenvolvedores e criadores de conteúdo
**Objetivo:** Ensinar a instalar e usar o sistema completo

---

## 🎯 INTRODUÇÃO (0:00 - 0:45)

### [TELA: Logo ou título do projeto]

**Narração:**

"Olá! Neste vídeo, você vai aprender a instalar e usar um sistema completo de geração automática de vídeos com sincronização labial perfeita.

Este sistema integra as mais avançadas tecnologias de IA do mercado: o Gemini da Google para formatação de texto, o ElevenLabs para síntese de voz de alta qualidade, e o WaveSpeed Wan 2.2 para criar vídeos com lip-sync realista.

Com apenas alguns cliques, você transforma um roteiro de texto em vídeos profissionais com apresentadores virtuais. Vamos começar!"

---

## 🔧 PRÉ-REQUISITOS (0:45 - 2:00)

### [TELA: Checklist com ícones]

**Narração:**

"Antes de começar, você vai precisar de:

**Primeiro:** Python 3.8 ou superior instalado no seu computador. Se você ainda não tem, acesse python.org e baixe a versão mais recente.

**Segundo:** FFmpeg instalado no sistema. O FFmpeg é essencial para a concatenação dos vídeos finais. No Windows, você pode baixar do site oficial. No Mac, use o Homebrew com o comando 'brew install ffmpeg'. E no Linux, use o gerenciador de pacotes da sua distribuição.

**Terceiro:** As chaves de API das três plataformas que vamos usar:
- Gemini API key - Acesse ai.google.dev
- ElevenLabs API key - Acesse elevenlabs.io
- WaveSpeed API key - Acesse wavespeed.ai

Anote essas chaves, pois vamos precisar delas na configuração.

**E por último:** Pelo menos 2GB de espaço livre em disco para os arquivos temporários e vídeos gerados."

---

## 📥 DOWNLOAD E INSTALAÇÃO (2:00 - 4:30)

### [TELA: Terminal/prompt de comando]

**Narração:**

"Agora vamos ao download e instalação. Existem duas formas de fazer isso.

### **OPÇÃO 1: Instalação Rápida no Windows**

Se você usa Windows, o processo é super simples.

Primeiro, faça o download do repositório do GitHub. Acesse github.com/[seu-usuario]/Automation-Ugc e clique em 'Code', depois 'Download ZIP'.

Extraia o arquivo ZIP em uma pasta de sua preferência.

Agora, navegue até a pasta extraída e procure o arquivo 'install.bat'.

Dê um clique duplo neste arquivo. Ele vai criar automaticamente o ambiente virtual, instalar todas as dependências necessárias, e já preparar tudo para você.

Aguarde alguns minutos enquanto as bibliotecas são instaladas. Você verá um monte de texto passando na tela - isso é normal!

### **OPÇÃO 2: Instalação Manual (Windows, Mac ou Linux)**

Se você prefere fazer manualmente ou usa Mac ou Linux, abra o terminal na pasta do projeto e execute:

Primeiro, crie um ambiente virtual com:
```
python -m venv venv
```

Depois, ative o ambiente virtual:
- No Windows: `venv\\Scripts\\activate`
- No Mac/Linux: `source venv/bin/activate`

E por fim, instale as dependências:
```
pip install -r requirements.txt
```

Pronto! Todas as bibliotecas necessárias estão instaladas."

---

## ⚙️ CONFIGURAÇÃO DAS API KEYS (4:30 - 6:00)

### [TELA: Arquivo .env sendo editado]

**Narração:**

"Agora vem a parte mais importante: configurar suas chaves de API.

Na pasta do projeto, você vai encontrar um arquivo chamado '.env.example'.

Renomeie este arquivo para apenas '.env' - removendo o '.example' do final.

Agora abra o arquivo '.env' com seu editor de texto favorito - pode ser o Notepad, VSCode, ou qualquer outro.

Você verá três linhas que precisam ser preenchidas:

```
GEMINI_API_KEY=sua_chave_aqui
ELEVENLABS_API_KEY=sua_chave_aqui
WAVESPEED_API_KEY=sua_chave_aqui
```

Substitua 'sua_chave_aqui' pelas chaves reais que você obteve nos sites das APIs.

**IMPORTANTE:** Certifique-se de não deixar espaços antes ou depois das chaves. Cole diretamente após o sinal de igual.

Por exemplo:
```
GEMINI_API_KEY=AIzaSyABC123def456GHI789
ELEVENLABS_API_KEY=sk_abc123def456ghi789
WAVESPEED_API_KEY=ws_xyz789abc456def123
```

Salve o arquivo e feche o editor.

Para garantir que tudo está funcionando, você pode executar o script de validação:
```
python check_api_keys.py
```

Este script vai testar todas as suas chaves e confirmar se estão válidas. Se tudo estiver ok, você verá mensagens de sucesso para cada API!"

---

## 🚀 PRIMEIRO USO (6:00 - 7:30)

### [TELA: Interface Gradio sendo iniciada]

**Narração:**

"Perfeito! Agora vamos iniciar o sistema pela primeira vez.

No Windows, basta dar um clique duplo no arquivo 'start.bat' que está na pasta do projeto.

Se você usa Mac ou Linux, ou prefere fazer manualmente, abra o terminal, ative o ambiente virtual e execute:
```
python app.py
```

Aguarde alguns segundos. Você verá várias mensagens de inicialização no terminal.

Quando tudo estiver pronto, uma janela do navegador vai abrir automaticamente com a interface do sistema. Se ela não abrir sozinha, copie o endereço que aparece no terminal - geralmente 'http://localhost:7860' - e cole no seu navegador.

E pronto! A interface está rodando e pronta para usar."

---

## 🎨 USANDO A INTERFACE (7:30 - 9:30)

### [TELA: Interface Gradio com cada elemento sendo destacado]

**Narração:**

"Vamos conhecer a interface. Ela é super intuitiva e dividida em áreas bem definidas.

### **Campo de Roteiro**

No topo, você tem uma grande caixa de texto. É aqui que você cola ou digita o roteiro completo do seu vídeo.

Pode escrever vários parágrafos - o sistema vai automaticamente dividir o texto em batches de 3 parágrafos cada e criar um vídeo para cada batch.

### **Seleção de Voz**

Logo abaixo, você escolhe a voz do apresentador. O sistema se conecta automaticamente ao ElevenLabs e lista todas as vozes disponíveis na sua conta.

Escolha a voz que melhor se encaixa no estilo do seu vídeo.

### **Modelo de Voz**

Aqui você pode escolher qual modelo do ElevenLabs usar:
- **Multilingual v2**: A melhor qualidade, suporta vários idiomas
- **Turbo v2.5**: Mais rápido, ideal para produção em massa
- E outras opções para casos específicos

### **Upload de Imagens**

Agora a parte visual! Faça upload de 1 a 20 imagens do apresentador virtual.

**DICA IMPORTANTE:** Use imagens de diferentes ângulos e expressões. O sistema vai variar automaticamente entre elas, criando vídeos mais dinâmicos e naturais.

As imagens devem ser em PNG ou JPG, de preferência em alta resolução.

### **Estimativa de Custo**

Antes de processar, você pode clicar em 'Estimar Custo e Tempo' para ter uma ideia de:
- Quantos vídeos serão gerados
- Tempo estimado de processamento
- Custo aproximado das APIs

Isso ajuda você a planejar melhor seu uso.

### **Processar!**

Quando tudo estiver pronto, clique no botão 'Gerar Vídeo'.

O sistema vai começar a processar. Você verá mensagens de progresso em tempo real:
- Formatando texto com IA...
- Gerando áudios com ElevenLabs...
- X vídeos na fila do WaveSpeed...
- Concatenando vídeos finais...

**IMPORTANTE:** Os vídeos são processados em paralelo na API WaveSpeed, então mesmo que você tenha 4 ou 5 vídeos, eles serão gerados simultaneamente, economizando muito tempo!

Quando tudo estiver concluído, o vídeo final aparecerá no player à direita. Você pode assistir diretamente na interface ou fazer o download clicando nos três pontinhos no canto do player."

---

## 💡 DICAS E BOAS PRÁTICAS (9:30 - 10:30)

### [TELA: Lista de dicas com ícones]

**Narração:**

"Antes de terminar, algumas dicas importantes para você tirar o máximo proveito do sistema:

**1. Qualidade das Imagens**
Use imagens de alta resolução, com boa iluminação e fundo limpo. Quanto melhor a imagem de entrada, melhor o resultado do lip-sync.

**2. Variação de Imagens**
Inclua imagens de diferentes ângulos. Isso deixa o vídeo final muito mais dinâmico e profissional.

**3. Tamanho do Texto**
Divida roteiros muito longos em múltiplas execuções. O sistema suporta até 50.000 caracteres, mas para melhor controle, trabalhe com seções menores.

**4. Escolha do Modelo**
Para português, use o Multilingual v2. Para produção em massa onde velocidade é prioridade, experimente o Turbo v2.5.

**5. Arquivos Temporários**
Os arquivos são salvos na pasta 'temp'. Você pode excluir essa pasta periodicamente para liberar espaço em disco.

**6. Logs**
Se algo der errado, os logs detalhados estão no terminal. Eles ajudam a identificar problemas."

---

## 🎓 CONCLUSÃO (10:30 - 11:00)

### [TELA: Resultado final - vídeo gerado]

**Narração:**

"E é isso! Você agora tem um sistema completo de geração de vídeos com IA rodando na sua máquina.

Este sistema combina:
- ✅ Formatação inteligente de texto com Gemini
- ✅ Síntese de voz realista com ElevenLabs
- ✅ Lip-sync perfeito com WaveSpeed
- ✅ Processamento paralelo para máxima eficiência

Se você tiver dúvidas, consulte os arquivos README.md, QUICKSTART.md e TROUBLESHOOTING.md na pasta do projeto. Eles têm informações detalhadas sobre todas as funcionalidades e solução de problemas comuns.

Gostou do vídeo? Deixe seu like e se inscreva no canal para mais tutoriais sobre automação e inteligência artificial!

Até a próxima!"

---

## 📝 NOTAS DE PRODUÇÃO

### Recursos Visuais Recomendados:

1. **Introdução:**
   - Animação do logo/título
   - Ícones das 3 APIs integradas
   - Exemplo de vídeo final gerado

2. **Pré-requisitos:**
   - Checklist animado
   - Screenshots dos sites das APIs
   - Ícones do Python e FFmpeg

3. **Instalação:**
   - Gravação de tela do processo completo
   - Destacar arquivos importantes (install.bat, requirements.txt)
   - Terminal com comandos sendo executados

4. **Configuração:**
   - Zoom no arquivo .env
   - Setas apontando para cada campo
   - Exemplo visual de chave válida vs inválida

5. **Interface:**
   - Gravação interativa da interface Gradio
   - Destaques (boxes/circles) em cada elemento
   - Transições suaves entre seções

6. **Conclusão:**
   - Montagem rápida de vários vídeos gerados
   - Call-to-action animado

### Música de Fundo Sugerida:
- Tom: Corporativo/tecnológico
- Volume: Baixo (não compete com narração)
- Estilo: Eletrônica suave ou lo-fi

### Edição:
- Cortes rápidos para manter dinamismo
- Text overlays com pontos-chave
- B-roll de exemplos práticos
- Zoom em detalhes importantes

---

## 🎤 SCRIPT ALTERNATIVO CURTO (3-5 minutos)

### Para quem prefere um vídeo mais direto:

**"Olá! Vou mostrar como instalar este gerador de vídeos com IA em apenas 3 passos.

Passo 1: Clone o repositório e execute 'install.bat'.

Passo 2: Copie o arquivo .env.example para .env e adicione suas API keys do Gemini, ElevenLabs e WaveSpeed.

Passo 3: Execute 'start.bat', cole seu roteiro, escolha a voz e modelo, faça upload das imagens e clique em Gerar.

Pronto! O sistema processa tudo automaticamente e entrega seu vídeo final. Simples assim!"**

---

**Fim do Roteiro**
