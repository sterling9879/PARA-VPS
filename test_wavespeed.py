"""
Script de diagnóstico para a API WaveSpeed
"""
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

def test_wavespeed_api():
    """Testa a API WaveSpeed com requisição simples"""

    print("="*60)
    print("🧪 DIAGNÓSTICO DA API WAVESPEED")
    print("="*60)
    print()

    api_key = os.getenv('WAVESPEED_API_KEY')

    if not api_key:
        print("❌ WAVESPEED_API_KEY não encontrada no .env")
        return

    print(f"✅ API Key encontrada: {api_key[:20]}...")
    print()

    # URLs de teste públicas (arquivos pequenos)
    test_audio_url = "https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav"
    test_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/240px-Cat03.jpg"

    print("📝 Usando arquivos de teste públicos:")
    print(f"   Áudio: {test_audio_url}")
    print(f"   Imagem: {test_image_url}")
    print()

    try:
        # Testa submissão de tarefa
        print("🔄 Submetendo tarefa de teste...")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "audio": test_audio_url,
            "image": test_image_url,
            "prompt": "",
            "resolution": "480p",
            "seed": -1
        }

        response = requests.post(
            "https://api.wavespeed.ai/api/v3/wavespeed-ai/wan-2.2/speech-to-video",
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"   Status Code: {response.status_code}")

        if response.status_code == 401:
            print("❌ ERRO 401: API KEY INVÁLIDA!")
            print()
            print("Sua WaveSpeed API Key está incorreta ou expirada.")
            print()
            print("Como obter uma chave válida:")
            print("1. Acesse: https://wavespeed.ai")
            print("2. Faça login")
            print("3. Vá em: Dashboard → API Keys")
            print("4. Copie ou crie uma nova chave")
            print("5. Cole no arquivo .env")
            return

        if response.status_code == 402:
            print("❌ ERRO 402: SEM CRÉDITOS!")
            print()
            print("Sua conta WaveSpeed não tem créditos suficientes.")
            print()
            print("Soluções:")
            print("1. Adicione créditos em: https://wavespeed.ai/pricing")
            print("2. Ou use o tier gratuito (verifique limites)")
            return

        if response.status_code == 429:
            print("❌ ERRO 429: RATE LIMIT!")
            print()
            print("Você atingiu o limite de requisições.")
            print()
            print("Soluções:")
            print("1. Aguarde alguns minutos")
            print("2. Verifique seu tier em: https://wavespeed.ai/dashboard")
            return

        response.raise_for_status()

        data = response.json()
        print("   ✅ Tarefa submetida com sucesso!")
        print()

        if data.get("code") != 200:
            print(f"⚠️  API retornou código: {data.get('code')}")
            print(f"   Mensagem: {data.get('message')}")
            print()
            print("Resposta completa:")
            print(data)
            return

        request_id = data.get("data", {}).get("id")
        print(f"   Request ID: {request_id}")
        print()

        # Aguarda processamento
        print("⏳ Aguardando 20 segundos antes de verificar resultado...")
        time.sleep(20)

        # Verifica resultado
        print("🔍 Verificando status da tarefa...")

        result_response = requests.get(
            f"https://api.wavespeed.ai/api/v3/predictions/{request_id}/result",
            headers=headers,
            timeout=30
        )

        result_response.raise_for_status()
        result_data = result_response.json()

        status = result_data.get("data", {}).get("status")
        print(f"   Status: {status}")
        print()

        if status == "failed":
            error_msg = result_data.get("data", {}).get("error", "Erro desconhecido")
            print("❌ TAREFA FALHOU!")
            print(f"   Erro: {error_msg}")
            print()
            print("Possíveis causas:")
            print("1. URLs dos arquivos inacessíveis pela API")
            print("2. Formato de arquivo incompatível")
            print("3. Problemas internos da API WaveSpeed")
            print()
            print("Resposta completa:")
            print(result_data)

        elif status == "completed":
            output_url = result_data.get("data", {}).get("outputs", [None])[0]
            print("✅ TAREFA CONCLUÍDA COM SUCESSO!")
            print(f"   Vídeo gerado: {output_url}")
            print()
            print("🎉 A API WaveSpeed está funcionando corretamente!")
            print("   O problema pode ser com os arquivos sendo enviados.")

        elif status == "processing":
            print("⏳ Tarefa ainda processando...")
            print("   A API está funcionando, mas precisa de mais tempo.")
            print("   (Vídeos podem levar 2-5 minutos)")

        else:
            print(f"⚠️  Status desconhecido: {status}")
            print("   Resposta completa:")
            print(result_data)

    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP: {e}")
        print(f"   Status: {e.response.status_code}")
        print(f"   Resposta: {e.response.text}")

    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_wavespeed_api()
