# Interface Web Moderna - Quick Start

## Instalação Rápida

```bash
# 1. Instalar dependências
pip install -r requirements-web.txt

# 2. Iniciar servidor
python web_server.py
```

## Acesso

Abra seu navegador em: **http://localhost:5000**

## Primeira Configuração

1. Clique em **"Configurar API Keys"** (canto superior direito)
2. Preencha suas chaves de API:
   - ElevenLabs API Key (opcional se usar MiniMax)
   - MiniMax API Key (opcional se usar ElevenLabs)
   - Gemini API Key (obrigatório)
   - WaveSpeed API Key (obrigatório)
3. Clique em **"Salvar Configurações"**

As chaves serão salvas automaticamente no arquivo `.env`

## Uso Básico

### Vídeo Único
1. Digite o roteiro
2. Selecione provedor e voz
3. Faça upload de imagens (PNG/JPG)
4. Ajuste workers simultâneos (1-10)
5. Clique em **"Gerar Vídeo"**

### Múltiplos Roteiros
1. Cole vários roteiros separados por `---`
2. Faça upload de imagens
3. Clique em **"Gerar Preview"**
4. Selecione voz para cada roteiro
5. Clique em **"Processar Todos"**

## Recursos

- ✨ Design moderno com dark mode
- 🔑 Configuração de API keys via interface
- 📊 Estimativa de custo antes de gerar
- 👁️ Preview de roteiros e batches
- 🖼️ Upload drag-and-drop
- 📹 Player de vídeo integrado

## Suporte

Para documentação completa, veja a pasta de artefatos ou consulte:
- `README.md` - Documentação geral
- `QUICKSTART.md` - Guia de instalação
