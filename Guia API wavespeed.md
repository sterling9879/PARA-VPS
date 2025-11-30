# **Guia Completo: API Wavespeed \- Wan 2.2 Speech-to-Video**

## **Índice**

1. [Introdução](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#introdu%C3%A7%C3%A3o)  
2. [Pré-requisitos](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#pr%C3%A9-requisitos)  
3. [O que é o Wan 2.2 Speech-to-Video](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#o-que-%C3%A9-o-wan-22-speech-to-video)  
4. [Autenticação](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#autentica%C3%A7%C3%A3o)  
5. [Estrutura da API](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#estrutura-da-api)  
6. [Exemplos de Uso](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#exemplos-de-uso)  
7. [Parâmetros da API](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#par%C3%A2metros-da-api)  
8. [Preços e Limites](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#pre%C3%A7os-e-limites)  
9. [Boas Práticas](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#boas-pr%C3%A1ticas)  
10. [Resolução de Problemas](https://claude.ai/chat/6b9ce2a3-9cbf-47fb-8665-7508a1e3c372#resolu%C3%A7%C3%A3o-de-problemas)

---

## **Introdução**

O **Wan 2.2 Speech-to-Video (S2V)** é um modelo de IA avançado que gera vídeos de alta qualidade a partir de imagens estáticas e áudio. O modelo cria expressões faciais realistas, movimentos corporais naturais e sincronização labial perfeita, ideal para aplicações em cinema, televisão, marketing digital e criação de avatares virtuais.

### **Principais Características**

* **Sincronização Labial Perfeita**: Utiliza o encoder de áudio Wav2Vec para entender nuances de fala  
* **Análise Visual Avançada**: Compreende anatomia humana, expressões faciais e movimentos corporais  
* **Movimentos Naturais**: Expressões faciais e linguagem corporal realistas  
* **Resolução Flexível**: Suporta 480p e 720p  
* **Duração Estendida**: Até 10 minutos de vídeo por geração  
* **API REST**: Sem cold starts, com preços acessíveis

---

## **Pré-requisitos**

### **1\. Criar uma Conta no WaveSpeedAI**

Acesse [https://wavespeed.ai](https://wavespeed.ai/) e crie sua conta.

### **2\. Obter uma API Key**

1. Faça login no dashboard do WaveSpeedAI  
2. Navegue até a seção "API Keys"  
3. Clique em "Criar Nova Chave" ou copie uma existente  
4. Guarde sua chave API em um local seguro

### **3\. Configurar a Chave API como Variável de Ambiente**

**Linux/macOS:**

export WAVESPEED\_API\_KEY="sua-chave-api-aqui"

**Windows (PowerShell):**

$env:WAVESPEED\_API\_KEY="sua-chave-api-aqui"

**Windows (CMD):**

set WAVESPEED\_API\_KEY=sua-chave-api-aqui

---

## **O que é o Wan 2.2 Speech-to-Video**

O Wan 2.2 S2V é construído sobre o modelo de difusão de vídeo Wan 2.2 e utiliza tecnologia avançada de IA para:

### **Análise de Áudio**

* Utiliza o encoder Wav2Vec para compreender ritmo, tom e padrões de pronúncia  
* Captura nuances sutis da fala

### **Compreensão Visual**

* Entende anatomia humana, expressões faciais e movimentos corporais  
* Baseado no robusto modelo de difusão de vídeo Wan 2.2

### **Sincronização Perfeita**

* Utiliza mecanismos sofisticados de atenção  
* Alinha perfeitamente movimentos labiais com o áudio  
* Mantém expressões faciais e linguagem corporal naturais

### **Seguimento de Instruções**

* Pode seguir prompts de texto para controlar cena, pose e comportamento geral  
* Mantém a sincronização de áudio simultaneamente

---

## **Autenticação**

Todas as requisições à API devem incluir sua chave API no header de autorização:

Authorization: Bearer ${WAVESPEED\_API\_KEY}

---

## **Estrutura da API**

### **Endpoint Base**

https://api.wavespeed.ai/api/v3/wavespeed-ai/wan-2.2/speech-to-video

### **Método HTTP**

* **POST**: Para submeter uma tarefa de geração de vídeo  
* **GET**: Para recuperar o resultado da tarefa

### **Fluxo de Trabalho**

1. **Submeter Tarefa**: Envie uma requisição POST com os parâmetros  
2. **Receber ID da Tarefa**: A API retorna um `requestId`  
3. **Consultar Resultado**: Use o `requestId` para verificar o status e obter o vídeo

---

## **Exemplos de Uso**

### **Exemplo 1: Requisição Básica com cURL**

#### **Passo 1: Submeter a Tarefa**

curl \--location \--request POST "https://api.wavespeed.ai/api/v3/wavespeed-ai/wan-2.2/speech-to-video" \\  
  \--header "Content-Type: application/json" \\  
  \--header "Authorization: Bearer ${WAVESPEED\_API\_KEY}" \\  
  \--data-raw '{  
    "image": "https://exemplo.com/sua-imagem.jpg",  
    "audio": "https://exemplo.com/seu-audio.mp3",  
    "prompt": "Uma pessoa falando calmamente para a câmera",  
    "resolution": "480p",  
    "seed": \-1  
  }'

**Resposta:**

{  
  "requestId": "abc123-def456-ghi789",  
  "status": "pending"  
}

#### **Passo 2: Consultar o Resultado**

curl \--location \--request GET "https://api.wavespeed.ai/api/v3/predictions/${requestId}/result" \\  
  \--header "Authorization: Bearer ${WAVESPEED\_API\_KEY}"

**Resposta de Sucesso:**

{  
  "requestId": "abc123-def456-ghi789",  
  "status": "completed",  
  "output": {  
    "video\_url": "https://wavespeed.ai/output/video123.mp4",  
    "duration": 15.5,  
    "resolution": "480p"  
  }  
}

### **Exemplo 2: Python com Requests**

import requests  
import time  
import os

\# Configuração  
API\_KEY \= os.getenv('WAVESPEED\_API\_KEY')  
BASE\_URL \= "https://api.wavespeed.ai/api/v3"  
ENDPOINT \= f"{BASE\_URL}/wavespeed-ai/wan-2.2/speech-to-video"

\# Headers  
headers \= {  
    "Content-Type": "application/json",  
    "Authorization": f"Bearer {API\_KEY}"  
}

\# Dados da requisição  
payload \= {  
    "image": "https://exemplo.com/pessoa.jpg",  
    "audio": "https://exemplo.com/audio.mp3",  
    "prompt": "Uma pessoa apresentando um produto com entusiasmo",  
    "resolution": "720p",  
    "seed": 42  
}

\# Submeter tarefa  
response \= requests.post(ENDPOINT, json=payload, headers=headers)  
result \= response.json()  
request\_id \= result\['requestId'\]

print(f"Tarefa submetida. ID: {request\_id}")

\# Consultar resultado  
status\_url \= f"{BASE\_URL}/predictions/{request\_id}/result"

while True:  
    status\_response \= requests.get(status\_url, headers=headers)  
    status\_data \= status\_response.json()  
      
    if status\_data\['status'\] \== 'completed':  
        print(f"Vídeo gerado: {status\_data\['output'\]\['video\_url'\]}")  
        break  
    elif status\_data\['status'\] \== 'failed':  
        print(f"Erro: {status\_data.get('error', 'Erro desconhecido')}")  
        break  
    else:  
        print(f"Status: {status\_data\['status'\]}. Aguardando...")  
        time.sleep(5)  \# Aguardar 5 segundos antes de consultar novamente

### **Exemplo 3: JavaScript/Node.js**

const fetch \= require('node-fetch');

const API\_KEY \= process.env.WAVESPEED\_API\_KEY;  
const BASE\_URL \= 'https://api.wavespeed.ai/api/v3';

async function generateVideo(imageUrl, audioUrl, prompt, resolution \= '480p') {  
  // Submeter tarefa  
  const submitResponse \= await fetch(  
    \`${BASE\_URL}/wavespeed-ai/wan-2.2/speech-to-video\`,  
    {  
      method: 'POST',  
      headers: {  
        'Content-Type': 'application/json',  
        'Authorization': \`Bearer ${API\_KEY}\`  
      },  
      body: JSON.stringify({  
        image: imageUrl,  
        audio: audioUrl,  
        prompt: prompt,  
        resolution: resolution,  
        seed: \-1  
      })  
    }  
  );

  const submitData \= await submitResponse.json();  
  const requestId \= submitData.requestId;  
    
  console.log(\`Tarefa submetida. ID: ${requestId}\`);

  // Consultar resultado  
  let status \= 'pending';  
  let videoUrl \= null;

  while (status \=== 'pending' || status \=== 'processing') {  
    await new Promise(resolve \=\> setTimeout(resolve, 5000)); // Aguardar 5s  
      
    const statusResponse \= await fetch(  
      \`${BASE\_URL}/predictions/${requestId}/result\`,  
      {  
        headers: {  
          'Authorization': \`Bearer ${API\_KEY}\`  
        }  
      }  
    );

    const statusData \= await statusResponse.json();  
    status \= statusData.status;

    if (status \=== 'completed') {  
      videoUrl \= statusData.output.video\_url;  
      console.log(\`Vídeo gerado: ${videoUrl}\`);  
    } else if (status \=== 'failed') {  
      console.error('Erro ao gerar vídeo:', statusData.error);  
    } else {  
      console.log(\`Status: ${status}\`);  
    }  
  }

  return videoUrl;  
}

// Uso  
generateVideo(  
  'https://exemplo.com/imagem.jpg',  
  'https://exemplo.com/audio.mp3',  
  'Uma pessoa falando sobre tecnologia',  
  '720p'  
);

---

## **Parâmetros da API**

### **Parâmetros de Entrada**

| Parâmetro | Tipo | Obrigatório | Descrição |
| ----- | ----- | ----- | ----- |
| `image` | string (URL) | ✅ Sim | URL da imagem estática (pessoa ou personagem). Formatos: JPG, PNG |
| `audio` | string (URL) | ✅ Sim | URL do arquivo de áudio (fala ou canto). Formatos: MP3, WAV |
| `prompt` | string | ❌ Não | Descrição textual para controlar cena, pose e comportamento |
| `resolution` | string | ❌ Não | Resolução do vídeo: `"480p"` ou `"720p"`. Padrão: `"480p"` |
| `seed` | integer | ❌ Não | Seed para geração determinística. Use `-1` para aleatório |

### **Recomendações para Imagens**

* **Qualidade**: Use imagens claras e bem iluminadas  
* **Enquadramento**: Funciona melhor com retratos, meio corpo ou corpo inteiro  
* **Fundo**: Fundos simples produzem melhores resultados  
* **Resolução**: Mínimo 512x512 pixels

### **Recomendações para Áudio**

* **Qualidade**: Use áudio claro, sem muito ruído de fundo  
* **Duração**: Até 10 minutos  
* **Formatos**: MP3, WAV  
* **Idiomas**: Suporta múltiplos idiomas

### **Parâmetros de Saída**

| Campo | Tipo | Descrição |
| ----- | ----- | ----- |
| `requestId` | string | ID único da tarefa |
| `status` | string | Status: `pending`, `processing`, `completed`, `failed` |
| `output.video_url` | string | URL do vídeo gerado (quando status \= completed) |
| `output.duration` | float | Duração do vídeo em segundos |
| `output.resolution` | string | Resolução do vídeo gerado |

---

## **Preços e Limites**

### **Preços**

* **480p**: $0.15 por 5 segundos de vídeo  
* **720p**: $0.30 por 5 segundos de vídeo

### **Exemplo de Cálculo**

Para um vídeo de 30 segundos em 720p:

30 segundos ÷ 5 \= 6 unidades  
6 × $0.30 \= $1.80

### **Limites**

* **Duração Máxima**: 10 minutos (600 segundos) por vídeo  
* **Duração Mínima**: 2 segundos (tanto para áudio quanto para vídeo)  
* **Créditos**: Verifique seu saldo no dashboard

**Observação**: Para $10, você pode gerar aproximadamente 66 vídeos de 5 segundos em 480p.

---

## **Boas Práticas**

### **1\. Otimização de Custos**

* **Comece com 480p** para testes e prototipagem  
* **Use 720p** apenas para produção final  
* **Teste com vídeos curtos** antes de gerar vídeos longos

### **2\. Qualidade de Entrada**

* **Imagens**: Use fotos de alta qualidade, bem iluminadas e focadas  
* **Áudio**: Grave em ambiente silencioso, sem eco  
* **Evite cenas complexas**: Fundos simples funcionam melhor

### **3\. Gerenciamento de Requisições**

\# Exemplo de retry com backoff exponencial  
import time

def submit\_with\_retry(payload, max\_retries=3):  
    for attempt in range(max\_retries):  
        try:  
            response \= requests.post(ENDPOINT, json=payload, headers=headers)  
            response.raise\_for\_status()  
            return response.json()  
        except requests.exceptions.RequestException as e:  
            if attempt \== max\_retries \- 1:  
                raise  
            wait\_time \= 2 \*\* attempt  
            print(f"Tentativa {attempt \+ 1} falhou. Aguardando {wait\_time}s...")  
            time.sleep(wait\_time)

### **4\. Uso de Webhooks (Recomendado para Produção)**

Para evitar polling constante, configure webhooks:

curl \--location \--request POST "https://api.wavespeed.ai/api/v3/wavespeed-ai/wan-2.2/speech-to-video?webhook\_url=https://seu-site.com/webhook" \\  
  \--header "Content-Type: application/json" \\  
  \--header "Authorization: Bearer ${WAVESPEED\_API\_KEY}" \\  
  \--data-raw '{...}'

### **5\. Armazenamento de Resultados**

* **URLs temporárias**: Os vídeos ficam disponíveis por 24 horas  
* **Faça download imediatamente**: Salve os vídeos em seu próprio servidor/storage  
* **Use CDN**: Para distribuição de vídeos em produção

---

## **Resolução de Problemas**

### **Erro: "Autenticação Inválida"**

**Solução**: Verifique se sua API key está correta e ativa

echo $WAVESPEED\_API\_KEY  \# Deve mostrar sua chave

### **Erro: "Imagem não encontrada"**

**Solução**:

* Certifique-se de que a URL da imagem é acessível publicamente  
* Teste a URL no navegador  
* Use URLs HTTPS sempre que possível

### **Erro: "Áudio muito curto"**

**Solução**: O áudio e vídeo devem ter pelo menos 2 segundos de duração.

### **Erro: "Saldo insuficiente"**

**Solução**: Adicione créditos à sua conta no dashboard do WaveSpeedAI.

### **Tarefa com Status "Failed"**

**Possíveis causas**:

* Imagem não contém um rosto detectável  
* Áudio corrompido ou formato inválido  
* Parâmetros inválidos

**Solução**: Verifique os dados de entrada e tente novamente.

### **Tempo de Processamento Longo**

**Normal**: Vídeos podem levar alguns minutos para serem processados, especialmente para resoluções mais altas e durações longas.

**Dica**: Use webhooks para evitar polling constante.

---

## **Recursos Adicionais**

### **Documentação Oficial**

* [WaveSpeedAI Docs](https://wavespeed.ai/docs)  
* [Página do Modelo](https://wavespeed.ai/models/wavespeed-ai/wan-2.2/speech-to-video)

### **Modelos Relacionados**

* **Wan 2.2 Image-to-Video**: Para criar vídeos sem áudio  
* **Wan 2.2 Text-to-Video**: Para gerar vídeos a partir de texto  
* **Wan 2.2 Video Edit**: Para editar vídeos existentes

### **Comunidade e Suporte**

* Dashboard: [https://wavespeed.ai/dashboard](https://wavespeed.ai/dashboard)  
* Documentação completa: [https://wavespeed.ai/docs](https://wavespeed.ai/docs)

---

## **Exemplo Completo de Aplicação**

Aqui está um exemplo completo de uma aplicação Python que usa a API:

import requests  
import time  
import os  
from typing import Optional

class WavespeedS2V:  
    def \_\_init\_\_(self, api\_key: str):  
        self.api\_key \= api\_key  
        self.base\_url \= "https://api.wavespeed.ai/api/v3"  
        self.headers \= {  
            "Content-Type": "application/json",  
            "Authorization": f"Bearer {api\_key}"  
        }  
      
    def generate\_video(  
        self,  
        image\_url: str,  
        audio\_url: str,  
        prompt: Optional\[str\] \= None,  
        resolution: str \= "480p",  
        seed: int \= \-1,  
        poll\_interval: int \= 5  
    ) \-\> dict:  
        """  
        Gera um vídeo usando o modelo Wan 2.2 Speech-to-Video  
          
        Args:  
            image\_url: URL da imagem de entrada  
            audio\_url: URL do áudio de entrada  
            prompt: Descrição opcional para controlar o vídeo  
            resolution: "480p" ou "720p"  
            seed: Seed para reprodutibilidade (-1 para aleatório)  
            poll\_interval: Intervalo de polling em segundos  
              
        Returns:  
            dict com informações do vídeo gerado  
        """  
        \# Submeter tarefa  
        endpoint \= f"{self.base\_url}/wavespeed-ai/wan-2.2/speech-to-video"  
        payload \= {  
            "image": image\_url,  
            "audio": audio\_url,  
            "resolution": resolution,  
            "seed": seed  
        }  
          
        if prompt:  
            payload\["prompt"\] \= prompt  
          
        print(f"Submetendo tarefa...")  
        response \= requests.post(endpoint, json=payload, headers=self.headers)  
        response.raise\_for\_status()  
          
        result \= response.json()  
        request\_id \= result\['requestId'\]  
        print(f"Tarefa submetida com ID: {request\_id}")  
          
        \# Consultar resultado  
        status\_url \= f"{self.base\_url}/predictions/{request\_id}/result"  
          
        while True:  
            time.sleep(poll\_interval)  
              
            status\_response \= requests.get(status\_url, headers=self.headers)  
            status\_response.raise\_for\_status()  
            status\_data \= status\_response.json()  
              
            status \= status\_data.get('status')  
            print(f"Status: {status}")  
              
            if status \== 'completed':  
                print(f"Vídeo gerado com sucesso\!")  
                return status\_data\['output'\]  
            elif status \== 'failed':  
                error \= status\_data.get('error', 'Erro desconhecido')  
                raise Exception(f"Geração falhou: {error}")  
            elif status not in \['pending', 'processing'\]:  
                raise Exception(f"Status inesperado: {status}")

\# Uso  
if \_\_name\_\_ \== "\_\_main\_\_":  
    api\_key \= os.getenv('WAVESPEED\_API\_KEY')  
    if not api\_key:  
        raise ValueError("WAVESPEED\_API\_KEY não configurada")  
      
    client \= WavespeedS2V(api\_key)  
      
    try:  
        output \= client.generate\_video(  
            image\_url="https://exemplo.com/pessoa.jpg",  
            audio\_url="https://exemplo.com/fala.mp3",  
            prompt="Uma pessoa apresentando com confiança",  
            resolution="720p"  
        )  
          
        print(f"\\n✅ Vídeo disponível em: {output\['video\_url'\]}")  
        print(f"📹 Duração: {output\['duration'\]}s")  
        print(f"📐 Resolução: {output\['resolution'\]}")  
          
    except Exception as e:  
        print(f"❌ Erro: {e}")

---

## **Conclusão**

O Wan 2.2 Speech-to-Video é uma ferramenta poderosa para criar vídeos de avatares falantes com sincronização labial realista. Com este guia, você deve ser capaz de:

✅ Configurar sua conta e API key  
 ✅ Fazer requisições básicas à API  
 ✅ Processar os resultados  
 ✅ Implementar boas práticas de produção  
 ✅ Resolver problemas comuns

Para dúvidas e suporte adicional, consulte a [documentação oficial](https://wavespeed.ai/docs) ou entre em contato com o suporte do WaveSpeedAI.

---

**Última atualização**: Novembro 2025  
 **Versão do Modelo**: Wan 2.2 Speech-to-Video  
 **Versão da API**: v3

