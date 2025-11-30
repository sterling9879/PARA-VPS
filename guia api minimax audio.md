# **Guia Completo: API do MiniMax Audio**

## **Índice**

1. [Introdução](https://claude.ai/chat/44d1d686-669e-4a41-95eb-0ac9b4c384e8#introdu%C3%A7%C3%A3o)  
2. [Configuração Inicial](https://claude.ai/chat/44d1d686-669e-4a41-95eb-0ac9b4c384e8#configura%C3%A7%C3%A3o-inicial)  
3. [Text-to-Speech (TTS)](https://claude.ai/chat/44d1d686-669e-4a41-95eb-0ac9b4c384e8#text-to-speech-tts)  
4. [Clonagem de Voz](https://claude.ai/chat/44d1d686-669e-4a41-95eb-0ac9b4c384e8#clonagem-de-voz)  
5. [Exemplos Práticos](https://claude.ai/chat/44d1d686-669e-4a41-95eb-0ac9b4c384e8#exemplos-pr%C3%A1ticos)  
6. [Referência de Parâmetros](https://claude.ai/chat/44d1d686-669e-4a41-95eb-0ac9b4c384e8#refer%C3%AAncia-de-par%C3%A2metros)  
7. [Melhores Práticas](https://claude.ai/chat/44d1d686-669e-4a41-95eb-0ac9b4c384e8#melhores-pr%C3%A1ticas)

---

## **Introdução**

A API do MiniMax Audio oferece capacidades avançadas de síntese de fala (Text-to-Speech) e clonagem de voz. Com suporte para mais de 40 idiomas e múltiplas emoções, é ideal para diversas aplicações como chatbots, assistentes virtuais, criação de conteúdo e muito mais.

### **Principais Recursos**

* **Síntese de Fala em Alta Qualidade**: Modelos HD e Turbo para diferentes necessidades  
* **Clonagem de Voz**: Clone vozes a partir de 10 segundos de áudio  
* **Suporte Multilíngue**: 40+ idiomas incluindo português, inglês, espanhol, chinês, etc.  
* **7 Emoções**: happy, sad, angry, fearful, disgusted, surprised, neutral  
* **Formatos Flexíveis**: MP3, PCM, FLAC, WAV  
* **Streaming**: Resposta em tempo real para aplicações interativas

---

## **Configuração Inicial**

### **1\. Obter Credenciais de API**

Para começar a usar a API do MiniMax Audio, você precisa:

1. Acesse o site oficial: https://platform.minimax.io  
2. Faça login ou crie uma conta  
3. Navegue até **Account → Your Profile** para encontrar seu **GroupID**  
4. Vá em **API Keys** e clique em **Create New Secret Key**  
5. Copie e armazene sua **API Key** com segurança (ela não será mostrada novamente)

### **2\. Endpoints da API**

**Endpoint Base**: `https://api.minimax.io`

Existem diferentes hosts dependendo da sua região:

* China: `https://api.minimax.io`  
* Global: `https://api.minimaxi.com` ou `https://api.minimaxi.chat`

**Importante**: A chave de API deve corresponder ao host utilizado.

### **3\. Autenticação**

Todas as requisições requerem autenticação via Bearer Token:

Authorization: Bearer YOUR\_API\_KEY  
Content-Type: application/json

---

## **Text-to-Speech (TTS)**

### **Modelos Disponíveis**

| Modelo | Descrição | Uso Recomendado |
| ----- | ----- | ----- |
| **speech-2.6-hd** | Alta definição com qualidade premium | Produção profissional, conteúdo de mídia |
| **speech-2.6-turbo** | Baixa latência otimizada | Aplicações em tempo real, chatbots |
| **speech-02-hd** | Alta qualidade com ritmo superior | Versão anterior HD |
| **speech-02-turbo** | Rápido e econômico | Aplicações de custo-efetivo |

### **Endpoint Principal**

POST https://api.minimax.io/v1/t2a\_v2

### **Exemplo Básico de Requisição**

curl \-X POST https://api.minimax.io/v1/t2a\_v2 \\  
  \-H "Authorization: Bearer YOUR\_API\_KEY" \\  
  \-H "Content-Type: application/json" \\  
  \-d '{  
    "model": "speech-2.6-hd",  
    "text": "Bem-vindo à API de Áudio do MiniMax. Transforme seu texto em fala natural e expressiva.",  
    "voice\_id": "male-qn-qingse",  
    "speed": 1.0,  
    "vol": 1.0,  
    "pitch": 0,  
    "audio\_sample\_rate": 32000,  
    "bitrate": 128000,  
    "format": "mp3"  
  }'

### **Exemplo em Python**

import requests  
import base64

def text\_to\_speech(text, voice\_id="male-qn-qingse"):  
    url \= "https://api.minimax.io/v1/t2a\_v2"  
      
    headers \= {  
        "Authorization": "Bearer YOUR\_API\_KEY",  
        "Content-Type": "application/json"  
    }  
      
    payload \= {  
        "model": "speech-2.6-hd",  
        "text": text,  
        "voice\_id": voice\_id,  
        "speed": 1.0,  
        "vol": 1.0,  
        "pitch": 0,  
        "audio\_sample\_rate": 32000,  
        "bitrate": 128000,  
        "format": "mp3"  
    }  
      
    response \= requests.post(url, headers=headers, json=payload)  
      
    if response.status\_code \== 200:  
        result \= response.json()  
        audio\_base64 \= result.get("audio\_file")  
          
        \# Decodificar e salvar o áudio  
        audio\_data \= base64.b64decode(audio\_base64)  
        with open("output.mp3", "wb") as f:  
            f.write(audio\_data)  
          
        print("Áudio gerado com sucesso\!")  
        return result  
    else:  
        print(f"Erro: {response.status\_code}")  
        print(response.text)  
        return None

\# Uso  
text\_to\_speech("Olá, esta é uma demonstração da API MiniMax Audio em português\!")

### **Exemplo em JavaScript/Node.js**

const axios \= require('axios');  
const fs \= require('fs');

async function textToSpeech(text, voiceId \= 'male-qn-qingse') {  
  const url \= 'https://api.minimax.io/v1/t2a\_v2';  
    
  const headers \= {  
    'Authorization': 'Bearer YOUR\_API\_KEY',  
    'Content-Type': 'application/json'  
  };  
    
  const payload \= {  
    model: 'speech-2.6-hd',  
    text: text,  
    voice\_id: voiceId,  
    speed: 1.0,  
    vol: 1.0,  
    pitch: 0,  
    audio\_sample\_rate: 32000,  
    bitrate: 128000,  
    format: 'mp3'  
  };  
    
  try {  
    const response \= await axios.post(url, payload, { headers });  
      
    if (response.status \=== 200\) {  
      const audioBase64 \= response.data.audio\_file;  
      const audioBuffer \= Buffer.from(audioBase64, 'base64');  
        
      fs.writeFileSync('output.mp3', audioBuffer);  
      console.log('Áudio gerado com sucesso\!');  
        
      return response.data;  
    }  
  } catch (error) {  
    console.error('Erro:', error.message);  
    return null;  
  }  
}

// Uso  
textToSpeech('Olá, esta é uma demonstração da API MiniMax Audio\!');

### **Resposta da API**

{  
  "audio\_file": "base64\_encoded\_audio\_data",  
  "trace\_id": "abc123-def456-ghi789",  
  "base\_resp": {  
    "status\_code": 0,  
    "status\_msg": "success"  
  }  
}

---

## **Clonagem de Voz**

### **Características**

* Clone vozes a partir de 10 segundos até 5 minutos de áudio  
* Formatos suportados: MP3, M4A, WAV  
* 99% de similaridade vocal reportada  
* Suporte para redução de ruído e normalização de volume

### **Endpoint de Clonagem**

POST https://api.minimax.io/v1/voice\_clone

### **Exemplo de Requisição**

curl \-X POST https://api.minimax.io/v1/voice\_clone \\  
  \-H "Authorization: Bearer YOUR\_API\_KEY" \\  
  \-H "Content-Type: application/json" \\  
  \-d '{  
    "file\_id": "YOUR\_UPLOADED\_FILE\_ID",  
    "voice\_id": "minha-voz-personalizada-01",  
    "model": "speech-2.6-hd",  
    "text": "Este é um teste da voz clonada.",  
    "need\_noise\_reduction": false,  
    "need\_volumn\_normalization": false  
  }'

### **Exemplo em Python (Clonagem de Voz)**

import requests

def clone\_voice(file\_id, custom\_voice\_id, preview\_text):  
    url \= "https://api.minimax.io/v1/voice\_clone"  
      
    headers \= {  
        "Authorization": "Bearer YOUR\_API\_KEY",  
        "Content-Type": "application/json"  
    }  
      
    payload \= {  
        "file\_id": file\_id,  
        "voice\_id": custom\_voice\_id,  
        "model": "speech-2.6-hd",  
        "text": preview\_text,  
        "need\_noise\_reduction": True,  
        "need\_volumn\_normalization": True  
    }  
      
    response \= requests.post(url, headers=headers, json=payload)  
      
    if response.status\_code \== 200:  
        print(f"Voz clonada com sucesso\! ID: {custom\_voice\_id}")  
        return response.json()  
    else:  
        print(f"Erro: {response.status\_code}")  
        print(response.text)  
        return None

\# Uso  
clone\_voice(  
    file\_id="uploaded\_file\_123",   
    custom\_voice\_id="minha-voz-01",  
    preview\_text="Olá, esta é minha voz clonada\!"  
)

---

## **Exemplos Práticos**

### **1\. Adicionar Pausas no Texto**

Você pode adicionar pausas personalizadas no texto usando a marcação `<#x#>`, onde `x` é a duração da pausa em segundos (de 0.01 a 99.99).

text \= """  
Olá, bem-vindo ao tutorial. \<\#1.5\#\>  
Hoje vamos aprender sobre a API MiniMax. \<\#0.5\#\>  
Vamos começar\!  
"""

text\_to\_speech(text)

### **2\. Usar Diferentes Emoções**

def text\_to\_speech\_with\_emotion(text, emotion="happy"):  
    payload \= {  
        "model": "speech-2.6-hd",  
        "text": text,  
        "voice\_id": "female-yujie",  
        "emotion": emotion,  \# happy, sad, angry, fearful, disgusted, surprised, neutral  
        "speed": 1.0,  
        "vol": 1.0,  
        "pitch": 0,  
        "audio\_sample\_rate": 32000,  
        "bitrate": 128000,  
        "format": "mp3"  
    }  
      
    \# ... resto do código

### **3\. Ajustar Velocidade e Tom**

\# Voz mais rápida e aguda  
payload \= {  
    "model": "speech-2.6-hd",  
    "text": "Texto mais rápido e agudo",  
    "voice\_id": "male-qn-qingse",  
    "speed": 1.5,      \# Velocidade: 0.5 \- 2.0  
    "vol": 1.0,        \# Volume: 0.1 \- 10.0  
    "pitch": 5,        \# Tom: \-12 a 12  
    "audio\_sample\_rate": 32000,  
    "bitrate": 128000,  
    "format": "mp3"  
}

### **4\. Gerar Áudio de Alta Qualidade**

\# Configuração para máxima qualidade  
payload \= {  
    "model": "speech-2.6-hd",  
    "text": "Áudio de alta qualidade",  
    "voice\_id": "female-tianmei",  
    "audio\_sample\_rate": 44100,  \# Taxa de amostragem mais alta  
    "bitrate": 320000,           \# Bitrate máximo  
    "format": "flac"             \# Formato sem perdas  
}

---

## **Referência de Parâmetros**

### **Parâmetros de Text-to-Speech**

| Parâmetro | Tipo | Descrição | Obrigatório | Padrão |
| ----- | ----- | ----- | ----- | ----- |
| `model` | string | Modelo a usar (speech-2.6-hd, speech-2.6-turbo, etc.) | Sim | \- |
| `text` | string | Texto a sintetizar (máx. 10.000 caracteres) | Sim | \- |
| `voice_id` | string | ID da voz do sistema ou voz clonada | Sim | \- |
| `speed` | float | Velocidade da fala (0.5 \- 2.0) | Não | 1.0 |
| `vol` | float | Nível de volume (0.1 \- 10.0) | Não | 1.0 |
| `pitch` | int | Ajuste de tom (-12 a 12\) | Não | 0 |
| `format` | string | Formato de saída (mp3, pcm, flac, wav) | Não | mp3 |
| `audio_sample_rate` | int | Taxa de amostragem (8000, 16000, 22050, 24000, 32000, 44100\) | Não | 32000 |
| `bitrate` | int | Bitrate (64000, 96000, 128000, 160000, 192000, 224000, 256000, 320000\) | Não | 128000 |
| `emotion` | string | Emoção (happy, sad, angry, fearful, disgusted, surprised, neutral) | Não | neutral |
| `channel` | int | Canais de áudio (1 ou 2\) | Não | 1 |

### **Idiomas Suportados**

A API suporta mais de 40 idiomas, incluindo:

* Português (Portuguese)  
* Inglês (English) \- US, UK, Austrália, Índia  
* Espanhol (Spanish)  
* Chinês (Chinese) \- Mandarim e Cantonês  
* Japonês (Japanese)  
* Coreano (Korean)  
* Francês (French)  
* Alemão (German)  
* Italiano (Italian)  
* Russo (Russian)  
* Árabe (Arabic)  
* Hindi (Hindi)  
* Turco (Turkish)  
* E muitos outros...

### **Vozes Disponíveis**

A API oferece 300+ vozes pré-construídas. Alguns exemplos:

* `male-qn-qingse` \- Voz masculina  
* `female-yujie` \- Voz feminina  
* `female-tianmei` \- Voz feminina  
* `Wise_Woman` \- Voz feminina sábia

Para obter a lista completa de vozes disponíveis, consulte a documentação oficial ou use o endpoint de listagem de vozes.

---

## **Melhores Práticas**

### **1\. Otimização de Performance**

* Use o modelo `speech-2.6-turbo` para aplicações em tempo real  
* Use `speech-2.6-hd` quando a qualidade for prioridade  
* Escolha a taxa de amostragem e bitrate adequados ao seu caso de uso

### **2\. Gerenciamento de Texto**

* Limite o texto a 10.000 caracteres por requisição  
* Para textos longos, divida em partes menores  
* Use marcadores de pausa `<#x#>` para melhorar a naturalidade

### **3\. Tratamento de Erros**

import requests  
from time import sleep

def text\_to\_speech\_with\_retry(text, max\_retries=3):  
    for attempt in range(max\_retries):  
        try:  
            response \= requests.post(url, headers=headers, json=payload, timeout=30)  
              
            if response.status\_code \== 200:  
                return response.json()  
            elif response.status\_code \== 429:  \# Rate limit  
                wait\_time \= 2 \*\* attempt  \# Exponential backoff  
                print(f"Rate limit atingido. Aguardando {wait\_time}s...")  
                sleep(wait\_time)  
            else:  
                print(f"Erro {response.status\_code}: {response.text}")  
                return None  
                  
        except requests.exceptions.Timeout:  
            print(f"Timeout na tentativa {attempt \+ 1}")  
            if attempt \< max\_retries \- 1:  
                sleep(2)  
                  
    return None

### **4\. Segurança**

* **NUNCA** exponha sua API Key no código cliente  
* Use variáveis de ambiente para armazenar credenciais  
* Implemente rate limiting no seu backend  
* Monitore o uso da API para evitar custos inesperados

import os

API\_KEY \= os.getenv('MINIMAX\_API\_KEY')

### **5\. Streaming (para aplicações em tempo real)**

Para aplicações que precisam de resposta em tempo real, considere usar o endpoint de streaming:

\# Exemplo conceitual de streaming  
def stream\_text\_to\_speech(text):  
    \# Configure o endpoint de streaming  
    \# Processe os chunks de áudio conforme chegam  
    \# Reproduza o áudio progressivamente  
    pass

---

## **Recursos Adicionais**

### **Documentação Oficial**

* **Plataforma MiniMax**: https://platform.minimax.io  
* **Documentação da API**: https://platform.minimax.io/docs/api-reference/speech-t2a-intro  
* **Console da API**: https://platform.minimax.io/console

### **Bibliotecas e SDKs**

* **MiniMax MCP (Python)**: https://github.com/MiniMax-AI/MiniMax-MCP  
* **MiniMax MCP (JavaScript)**: https://github.com/MiniMax-AI/MiniMax-MCP-JS

### **Integrações de Terceiros**

* **fal.ai**: Acesso simplificado à API do MiniMax  
* **Replicate**: Plataforma de modelos de IA com suporte ao MiniMax  
* **AI/ML API**: Agregador de APIs de IA incluindo MiniMax

---

## **Solução de Problemas**

### **Erro: "Invalid API Key"**

* Verifique se a API Key está correta  
* Certifique-se de que está usando o host correto para sua região  
* A chave deve corresponder ao host (api.minimax.io ou api.minimaxi.com)

### **Erro: Rate Limit Excedido**

* Implemente backoff exponencial  
* Considere fazer upgrade do seu plano  
* Distribua as requisições ao longo do tempo

### **Áudio com Qualidade Ruim**

* Aumente o bitrate (até 320000\)  
* Use taxa de amostragem mais alta (44100)  
* Experimente o formato FLAC para melhor qualidade  
* Use o modelo HD ao invés do Turbo

### **Latência Alta**

* Use o modelo Turbo ao invés do HD  
* Reduza a taxa de amostragem e bitrate  
* Considere fazer cache de áudios comuns  
* Use o endpoint de streaming para resposta progressiva

---

## **Conclusão**

A API do MiniMax Audio é uma ferramenta poderosa para adicionar capacidades de síntese de fala e clonagem de voz às suas aplicações. Com suporte para múltiplos idiomas, emoções e vozes personalizadas, oferece flexibilidade para diversos casos de uso.

Para começar:

1. Crie sua conta em https://platform.minimax.io  
2. Obtenha sua API Key  
3. Experimente os exemplos deste guia  
4. Consulte a documentação oficial para recursos avançados

**Dica Final**: Sempre teste com pequenos volumes primeiro e monitore seus custos antes de escalar para produção\!

---

*Guia criado em novembro de 2025\. Para informações mais recentes, consulte a documentação oficial do MiniMax.*

