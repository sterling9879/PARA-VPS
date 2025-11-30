# **Guia Completo da API ElevenLabs**

*Text-to-Speech, Speech-to-Text, Music, Sound Effects e mais*

---

## **1\. Introdução**

A ElevenLabs é uma plataforma líder em tecnologia de áudio com inteligência artificial. Sua API permite criar vozes sintéticas extremamente realistas, transcrever áudio, gerar músicas e efeitos sonoros. Este guia cobre todos os modelos e funcionalidades disponíveis.

### **1.1 Funcionalidades Principais**

* **Text-to-Speech (TTS):** Converter texto em fala natural e expressiva  
* **Speech-to-Text (STT):** Transcrever áudio para texto com alta precisão  
* **Text-to-Dialogue:** Criar diálogos com múltiplos personagens  
* **Voice Cloning:** Clonar vozes a partir de amostras de áudio  
* **Music Generation:** Gerar músicas completas via prompts  
* **Sound Effects:** Criar efeitos sonoros com descrições  
* **Dubbing:** Dublar vídeos automaticamente  
* **Voice Agents:** Criar agentes de voz conversacionais

---

## **2\. Instalação e Configuração**

### **2.1 Obtendo sua API Key**

1. Acesse [elevenlabs.io](https://elevenlabs.io/) e crie uma conta gratuita  
2. Vá em **Profile Settings → API Keys**  
3. Clique em "Create API Key" e copie a chave  
4. Guarde a chave de forma segura (use variáveis de ambiente)

### **2.2 Instalação \- Python**

pip install elevenlabs

Para funcionalidades de áudio em tempo real:

pip install "elevenlabs\[pyaudio\]"

### **2.3 Instalação \- Node.js**

npm install elevenlabs

### **2.4 Configuração do Ambiente**

Crie um arquivo `.env` na raiz do seu projeto:

ELEVENLABS\_API\_KEY=sua\_api\_key\_aqui

---

## **3\. Modelos Disponíveis**

A ElevenLabs oferece diversos modelos otimizados para diferentes casos de uso. Os modelos `eleven_monolingual_v1` e `eleven_multilingual_v1` estão descontinuados.

### **3.1 Modelos de Text-to-Speech**

#### **Eleven v3 (`eleven_v3`)**

O modelo mais avançado da ElevenLabs, atualmente em alpha.

| Característica | Valor |
| ----- | ----- |
| Idiomas | 70+ |
| Limite de caracteres | 3.000 |
| Latência | Alta (não recomendado para tempo real) |

**Recursos:**

* Alta expressividade emocional e contextual  
* Suporte a diálogos com múltiplos personagens  
* Ideal para audiobooks, jogos e conteúdo dramático

---

#### **Multilingual v2 (`eleven_multilingual_v2`)**

Modelo de alta qualidade com excelente suporte multilíngue.

| Característica | Valor |
| ----- | ----- |
| Idiomas | 29 |
| Limite de caracteres | 10.000 |
| Qualidade | Muito alta |

**Recursos:**

* Qualidade de áudio superior e consistente  
* Melhor normalização de números e datas  
* Ideal para conteúdo profissional e e-learning

**Idiomas suportados:** Inglês, Japonês, Chinês, Alemão, Hindi, Francês, Coreano, Português, Italiano, Espanhol, Indonésio, Holandês, Turco, Filipino, Polonês, Sueco, Búlgaro, Romeno, Árabe, Tcheco, Grego, Finlandês, Croata, Malaio, Eslovaco, Dinamarquês, Tâmil, Ucraniano, Russo.

---

#### **Flash v2.5 (`eleven_flash_v2_5`)**

Modelo otimizado para velocidade e baixa latência.

| Característica | Valor |
| ----- | ----- |
| Idiomas | 32 |
| Limite de caracteres | 40.000 |
| Latência | \~75ms |
| Preço | 50% mais barato |

**Recursos:**

* Ultra-baixa latência  
* Ideal para chatbots, agentes de voz e aplicações em tempo real  
* Normalização de texto desabilitada por padrão

---

#### **Turbo v2.5 (`eleven_turbo_v2_5`)**

Equilíbrio entre qualidade e velocidade.

| Característica | Valor |
| ----- | ----- |
| Idiomas | 32 |
| Limite de caracteres | 40.000 |
| Latência | \~250-300ms |

**Recursos:**

* Qualidade superior ao Flash  
* Ideal quando qualidade é mais importante que latência mínima

---

### **3.2 Modelos de Speech-to-Text**

#### **Scribe v1 (`scribe_v1`)**

Modelo principal de transcrição.

| Característica | Valor |
| ----- | ----- |
| Idiomas | 99 |
| Máx. speakers | 32 |
| Tamanho máx. arquivo | 3GB |
| Duração máx. | 10 horas |

**Recursos:**

* Timestamps precisos por palavra  
* Diarização de speakers  
* Detecção de eventos de áudio (risos, aplausos, etc.)

---

#### **Scribe v2 Realtime (`scribe_v2_realtime`)**

Modelo para transcrição em tempo real.

| Característica | Valor |
| ----- | ----- |
| Idiomas | 92+ |
| Latência | \~150ms |
| Conexão | WebSocket |

**Recursos:**

* Streaming em tempo real  
* Voice Activity Detection (VAD) automático  
* Ideal para transcrição ao vivo e agentes de IA

---

### **3.3 Modelos de Música e Efeitos Sonoros**

#### **Eleven Music (`eleven_music`)**

| Característica | Valor |
| ----- | ----- |
| Duração | 10s \- 5min |
| Disponibilidade | Apenas usuários pagos |

**Recursos:**

* Geração via prompts em linguagem natural  
* Vocais ou apenas instrumental  
* Suporte multilíngue para letras  
* Edição por seções

---

#### **Text to Sound Effects**

| Característica | Valor |
| ----- | ----- |
| Duração máx. | 30 segundos |

**Recursos:**

* Suporte a loops contínuos  
* Controle de influência do prompt  
* Ideal para jogos, vídeos e podcasts

---

## **4\. Text-to-Speech (TTS)**

### **4.1 Exemplo Básico \- Python**

from dotenv import load\_dotenv  
from elevenlabs.client import ElevenLabs  
from elevenlabs.play import play

load\_dotenv()  
client \= ElevenLabs()

audio \= client.text\_to\_speech.convert(  
    text="Olá\! Este é um teste da API ElevenLabs.",  
    voice\_id="JBFqnCBsd6RMkjVDRZzb",  
    model\_id="eleven\_multilingual\_v2",  
    output\_format="mp3\_44100\_128",  
)

play(audio)

### **4.2 Streaming em Tempo Real**

from elevenlabs import stream  
from elevenlabs.client import ElevenLabs

client \= ElevenLabs()

audio\_stream \= client.text\_to\_speech.stream(  
    text="Este áudio é gerado em tempo real\!",  
    voice\_id="JBFqnCBsd6RMkjVDRZzb",  
    model\_id="eleven\_flash\_v2\_5"  
)

stream(audio\_stream)

### **4.3 Salvando em Arquivo**

from elevenlabs.client import ElevenLabs

client \= ElevenLabs()

audio \= client.text\_to\_speech.convert(  
    text="Texto para converter em áudio.",  
    voice\_id="JBFqnCBsd6RMkjVDRZzb",  
    model\_id="eleven\_multilingual\_v2",  
)

with open("audio.mp3", "wb") as f:  
    for chunk in audio:  
        f.write(chunk)

### **4.4 Chamada HTTP Direta (cURL)**

curl \-X POST "https://api.elevenlabs.io/v1/text-to-speech/{voice\_id}" \\  
  \-H "xi-api-key: SUA\_API\_KEY" \\  
  \-H "Content-Type: application/json" \\  
  \-d '{  
    "text": "Seu texto aqui",  
    "model\_id": "eleven\_multilingual\_v2",  
    "voice\_settings": {  
      "stability": 0.5,  
      "similarity\_boost": 0.75  
    }  
  }' \--output audio.mp3

### **4.5 Configurações de Voz (voice\_settings)**

| Parâmetro | Range | Recomendado | Descrição |
| ----- | ----- | ----- | ----- |
| `stability` | 0.0 \- 1.0 | 0.5 | Controla variabilidade. Baixo \= emotivo, Alto \= monótono |
| `similarity_boost` | 0.0 \- 1.0 | 0.75 | Proximidade à voz original. Muito alto pode reproduzir ruídos |
| `style` | 0.0 \- 1.0 | 0 | Exagero de estilo. Aumenta latência |
| `use_speaker_boost` | true/false | true | Aumenta similaridade. Aumenta levemente latência |

### **4.6 Formatos de Saída Disponíveis**

| Formato | Descrição | Requisito |
| ----- | ----- | ----- |
| `mp3_44100_128` | MP3 padrão, 44.1kHz, 128kbps | Default |
| `mp3_44100_192` | MP3 alta qualidade | Creator tier+ |
| `mp3_22050_32` | MP3 compacto | \- |
| `pcm_16000` | PCM 16kHz | \- |
| `pcm_22050` | PCM 22.05kHz | \- |
| `pcm_24000` | PCM 24kHz | \- |
| `pcm_44100` | PCM 44.1kHz | Pro tier+ |
| `ulaw_8000` | μ-law 8kHz (Twilio) | \- |

---

## **5\. Speech-to-Text (STT)**

### **5.1 Transcrição Básica**

from elevenlabs.client import ElevenLabs

client \= ElevenLabs()

result \= client.speech\_to\_text.convert(  
    file=open("audio.mp3", "rb"),  
    model\_id="scribe\_v1",  
    language\_code="pt",  
    diarize=True,  
    tag\_audio\_events=True  
)

print(result.text)

### **5.2 Transcrição de URL**

result \= client.speech\_to\_text.convert(  
    cloud\_storage\_url="https://exemplo.com/audio.mp3",  
    model\_id="scribe\_v1"  
)

### **5.3 Parâmetros Disponíveis**

| Parâmetro | Tipo | Descrição |
| ----- | ----- | ----- |
| `model_id` | string | `scribe_v1` ou `scribe_v1_experimental` |
| `language_code` | string | Código ISO (pt, en, es). Opcional \- detecta automaticamente |
| `diarize` | boolean | Identificar diferentes speakers (até 32\) |
| `num_speakers` | integer | Número esperado de speakers |
| `tag_audio_events` | boolean | Marcar eventos como (risos), (aplausos) |
| `include_timestamps` | boolean | Incluir timestamps por palavra |

---

## **6\. Voice Cloning**

### **6.1 Clonagem Instantânea**

from elevenlabs.client import ElevenLabs

client \= ElevenLabs(api\_key="SUA\_API\_KEY")

voice \= client.voices.ivc.create(  
    name="Minha Voz Clonada",  
    description="Voz masculina para narrações",  
    files=\["sample1.mp3", "sample2.mp3", "sample3.mp3"\]  
)

print(f"Voice ID: {voice.voice\_id}")

### **6.2 Usando a Voz Clonada**

audio \= client.text\_to\_speech.convert(  
    text="Agora estou usando minha voz clonada\!",  
    voice\_id=voice.voice\_id,  
    model\_id="eleven\_multilingual\_v2"  
)

### **6.3 Dicas para Melhor Qualidade**

* Use áudios de alta qualidade, sem ruído de fundo  
* Forneça 3-5 amostras de áudio diferentes  
* Amostras devem ter entre 30 segundos e 3 minutos  
* Varie o conteúdo das amostras (diferentes frases e emoções)  
* Evite música de fundo ou outros sons  
* Grave em ambiente silencioso

---

## **7\. Geração de Música**

O Eleven Music gera músicas de qualidade profissional via prompts. **Disponível apenas para usuários pagos.**

### **7.1 Geração Básica**

from elevenlabs.client import ElevenLabs

client \= ElevenLabs()

result \= client.music.compose(  
    prompt="Uma música pop animada em português, com vocais femininos e batida dançante sobre o verão",  
    duration\_ms=120000  \# 2 minutos  
)

with open("musica.mp3", "wb") as f:  
    for chunk in result:  
        f.write(chunk)

### **7.2 Com Plano de Composição Detalhado**

composition\_plan \= {  
    "sections": \[  
        {  
            "type": "intro",  
            "duration\_ms": 15000,  
            "description": "Intro suave com piano"  
        },  
        {  
            "type": "verse",  
            "duration\_ms": 30000,  
            "description": "Verso com vocais e violão"  
        },  
        {  
            "type": "chorus",  
            "duration\_ms": 30000,  
            "description": "Refrão energético"  
        },  
        {  
            "type": "outro",  
            "duration\_ms": 15000,  
            "description": "Fade out gradual"  
        }  
    \]  
}

result \= client.music.compose(composition\_plan=composition\_plan)

### **7.3 Streaming de Música**

result \= client.music.stream(  
    prompt="Música eletrônica ambiente para meditação"  
)

for chunk in result:  
    \# Processar chunks de áudio em tempo real  
    pass

---

## **8\. Sound Effects**

### **8.1 Gerando Efeitos Sonoros**

from elevenlabs.client import ElevenLabs

client \= ElevenLabs()

result \= client.text\_to\_sound\_effects.convert(  
    text="Trovão forte seguido de chuva intensa",  
    duration\_seconds=10,  
    prompt\_influence=0.3  
)

with open("efeito.mp3", "wb") as f:  
    for chunk in result:  
        f.write(chunk)

### **8.2 Parâmetros**

| Parâmetro | Tipo | Descrição |
| ----- | ----- | ----- |
| `text` | string | Descrição do efeito sonoro |
| `duration_seconds` | float | Duração (0.5 a 30 segundos) |
| `prompt_influence` | float | Influência do prompt (0.0 a 1.0, default: 0.3) |

### **8.3 Exemplos de Prompts**

\# Ambiente  
"Floresta tropical com pássaros cantando e vento nas árvores"

\# Ação  
"Espada sendo desembainhada seguida de golpes metálicos"

\# Urbano  
"Trânsito intenso de cidade grande com buzinas e motores"

\# Sci-fi  
"Porta de nave espacial abrindo com som pneumático"

---

## **9\. Dubbing (Dublagem)**

Duble vídeos e áudios automaticamente para outros idiomas.

### **9.1 Dublando um Arquivo**

from elevenlabs.client import ElevenLabs  
import time

client \= ElevenLabs()

\# Iniciar dublagem  
dubbing \= client.dubbing.create(  
    file=open("video.mp4", "rb"),  
    target\_lang="pt",  
    source\_lang="en"  
)

dubbing\_id \= dubbing.dubbing\_id  
print(f"Dubbing ID: {dubbing\_id}")

\# Aguardar conclusão (polling)  
while True:  
    status \= client.dubbing.get(dubbing\_id)  
    if status.status \== "completed":  
        break  
    elif status.status \== "failed":  
        raise Exception("Dublagem falhou")  
    time.sleep(10)

\# Baixar áudio dublado  
audio \= client.dubbing.get\_audio(dubbing\_id, "pt")  
with open("video\_dublado.mp4", "wb") as f:  
    f.write(audio)

### **9.2 Dublando de URL**

Suporta URLs do YouTube, TikTok, Twitter e Vimeo:

dubbing \= client.dubbing.create(  
    source\_url="https://www.youtube.com/watch?v=VIDEO\_ID",  
    target\_lang="pt",  
    source\_lang="en"  
)

---

## **10\. Gerenciamento de Vozes**

### **10.1 Listando Vozes Disponíveis**

from elevenlabs.client import ElevenLabs

client \= ElevenLabs(api\_key="SUA\_API\_KEY")

response \= client.voices.search()

for voice in response.voices:  
    print(f"{voice.name}: {voice.voice\_id}")

### **10.2 Obtendo Detalhes de uma Voz**

voice \= client.voices.get(voice\_id="JBFqnCBsd6RMkjVDRZzb")

print(f"Nome: {voice.name}")  
print(f"Categoria: {voice.category}")  
print(f"Labels: {voice.labels}")

### **10.3 Obtendo Configurações**

settings \= client.voices.get\_settings(voice\_id="JBFqnCBsd6RMkjVDRZzb")

print(f"Stability: {settings.stability}")  
print(f"Similarity: {settings.similarity\_boost}")

### **10.4 Atualizando Configurações**

client.voices.edit\_settings(  
    voice\_id="JBFqnCBsd6RMkjVDRZzb",  
    stability=0.5,  
    similarity\_boost=0.8  
)

### **10.5 Deletando uma Voz**

client.voices.delete(voice\_id="voice\_id\_para\_deletar")

---

## **11\. Uso Assíncrono**

### **11.1 Cliente Assíncrono**

import asyncio  
from elevenlabs.client import AsyncElevenLabs

async def main():  
    client \= AsyncElevenLabs(api\_key="SUA\_API\_KEY")  
      
    \# Listar modelos  
    models \= await client.models.list()  
    for model in models:  
        print(model.name)  
      
    \# Gerar áudio  
    audio \= await client.text\_to\_speech.convert(  
        text="Texto assíncrono\!",  
        voice\_id="JBFqnCBsd6RMkjVDRZzb",  
        model\_id="eleven\_flash\_v2\_5"  
    )

asyncio.run(main())

---

## **12\. Referência de Endpoints**

### **12.1 Text-to-Speech**

| Método | Endpoint | Descrição |
| ----- | ----- | ----- |
| POST | `/v1/text-to-speech/{voice_id}` | Gerar áudio |
| POST | `/v1/text-to-speech/{voice_id}/stream` | Streaming de áudio |
| POST | `/v1/text-to-speech/{voice_id}/with-timestamps` | Com timestamps |

### **12.2 Speech-to-Text**

| Método | Endpoint | Descrição |
| ----- | ----- | ----- |
| POST | `/v1/speech-to-text` | Transcrever áudio |

### **12.3 Voices**

| Método | Endpoint | Descrição |
| ----- | ----- | ----- |
| GET | `/v1/voices` | Listar vozes |
| GET | `/v1/voices/{voice_id}` | Obter detalhes |
| GET | `/v1/voices/{voice_id}/settings` | Obter configurações |
| POST | `/v1/voices/{voice_id}/settings/edit` | Editar configurações |
| DELETE | `/v1/voices/{voice_id}` | Deletar voz |
| POST | `/v1/voices/add` | Adicionar voz (clone) |

### **12.4 Music**

| Método | Endpoint | Descrição |
| ----- | ----- | ----- |
| POST | `/v1/music/compose` | Gerar música |
| POST | `/v1/music/stream` | Streaming de música |

### **12.5 Sound Effects**

| Método | Endpoint | Descrição |
| ----- | ----- | ----- |
| POST | `/v1/sound-generation` | Gerar efeito sonoro |

### **12.6 Dubbing**

| Método | Endpoint | Descrição |
| ----- | ----- | ----- |
| POST | `/v1/dubbing` | Criar dublagem |
| GET | `/v1/dubbing/{dubbing_id}` | Status da dublagem |
| GET | `/v1/dubbing/{dubbing_id}/audio/{language_code}` | Baixar áudio |
| DELETE | `/v1/dubbing/{dubbing_id}` | Deletar dublagem |

### **12.7 Models**

| Método | Endpoint | Descrição |
| ----- | ----- | ----- |
| GET | `/v1/models` | Listar modelos disponíveis |

### **12.8 User**

| Método | Endpoint | Descrição |
| ----- | ----- | ----- |
| GET | `/v1/user` | Informações do usuário |
| GET | `/v1/user/subscription` | Detalhes da assinatura |

---

## **13\. Boas Práticas e Dicas**

### **13.1 Otimização de Latência**

* Use **Flash v2.5** para aplicações em tempo real  
* Use **streaming** ao invés de aguardar o áudio completo  
* Defina `optimize_streaming_latency=3` para latência mínima  
* **Normalize números e datas** antes de enviar para o modelo  
* Use **WebSockets** para comunicação bidirecional

### **13.2 Qualidade de Áudio**

* Use **Multilingual v2** ou **Eleven v3** quando qualidade é prioridade  
* Ajuste `stability` (0.4-0.6) para vozes mais naturais  
* Mantenha `similarity_boost` em \~0.75 para evitar artefatos  
* Use **pontuação adequada** para melhor entonação  
* Quebre textos longos em **segmentos menores**

### **13.3 Segurança**

* **Nunca exponha** sua API key no frontend  
* Use **variáveis de ambiente** para armazenar credenciais  
* Implemente **rate limiting** em sua aplicação  
* **Monitore uso** da API para evitar custos inesperados  
* Use **HTTPS** em todas as requisições

### **13.4 Custos**

* **Flash v2.5** é 50% mais barato que outros modelos  
* **Regenerações** do mesmo texto (até 2x) são gratuitas  
* **Cache** áudios frequentemente usados  
* Use a **tier adequada** para seu volume de uso  
* Monitore seu **uso de caracteres** no dashboard

### **13.5 Prompts Eficientes**

\# ❌ Ruim \- texto não formatado  
"olá como você está tudo bem comigo e com você"

\# ✅ Bom \- pontuação adequada  
"Olá\! Como você está? Tudo bem comigo, e com você?"

\# ❌ Ruim \- números não normalizados (para Flash)  
"Ligue para 11999998888 às 14:30"

\# ✅ Bom \- números normalizados  
"Ligue para onze, nove, nove, nove, nove, nove, oito, oito, oito, oito às duas e meia da tarde"

---

## **14\. Solução de Problemas**

### **Erros Comuns**

| Erro | Causa | Solução |
| ----- | ----- | ----- |
| `401 Unauthorized` | API key inválida | Verifique a chave |
| `429 Too Many Requests` | Rate limit excedido | Aguarde ou upgrade de tier |
| `400 Bad Request` | Parâmetros inválidos | Verifique a documentação |
| `500 Internal Server Error` | Erro do servidor | Tente novamente |

### **Verificando sua API Key**

from elevenlabs.client import ElevenLabs

client \= ElevenLabs(api\_key="SUA\_API\_KEY")

try:  
    user \= client.user.get()  
    print(f"Usuário: {user.subscription.tier}")  
except Exception as e:  
    print(f"Erro: {e}")

---

## **Links Úteis**

* **Documentação oficial:** [elevenlabs.io/docs](https://elevenlabs.io/docs)  
* **API Reference:** [elevenlabs.io/docs/api-reference](https://elevenlabs.io/docs/api-reference)  
* **Voice Lab:** [elevenlabs.io/voice-lab](https://elevenlabs.io/voice-lab)  
* **Pricing:** [elevenlabs.io/pricing](https://elevenlabs.io/pricing)  
* **GitHub Python SDK:** [github.com/elevenlabs/elevenlabs-python](https://github.com/elevenlabs/elevenlabs-python)  
* **GitHub Node SDK:** [github.com/elevenlabs/elevenlabs-js](https://github.com/elevenlabs/elevenlabs-js)

---

*Guia atualizado em Novembro de 2025*

