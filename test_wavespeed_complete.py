"""
Teste completo do pipeline WaveSpeed com uploads compatíveis
"""
import os
import time
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from wavespeed_uploader import WaveSpeedCompatibleUploader
import requests

load_dotenv()

def create_test_files():
    """Cria arquivos de teste pequenos"""
    print("📝 Criando arquivos de teste...")

    # Cria um arquivo de áudio de teste (silêncio de 1 segundo)
    # WAV file simples: RIFF header + dados
    audio_data = b'RIFF' + b'\x00\x00\x00\x00' + b'WAVE'
    audio_data += b'fmt ' + b'\x10\x00\x00\x00' + b'\x01\x00\x01\x00' + b'\x22\x56\x00\x00'
    audio_data += b'\x44\xAC\x00\x00' + b'\x02\x00\x10\x00'
    audio_data += b'data' + (b'\x00' * 44100)  # 1 segundo de silêncio

    audio_file = Path(tempfile.gettempdir()) / "test_audio.wav"
    audio_file.write_bytes(audio_data)

    # Cria uma imagem de teste (PNG 1x1 pixel preto)
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
    png_data += b'\x00\x00\x00\x0cIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

    image_file = Path(tempfile.gettempdir()) / "test_image.png"
    image_file.write_bytes(png_data)

    print(f"  ✅ Áudio: {audio_file} ({len(audio_data):,} bytes)")
    print(f"  ✅ Imagem: {image_file} ({len(png_data):,} bytes)")
    print()

    return audio_file, image_file

def test_wavespeed_complete_pipeline():
    """Testa o pipeline completo: upload + WaveSpeed"""

    print("="*60)
    print("🧪 TESTE COMPLETO DO PIPELINE WAVESPEED")
    print("="*60)
    print()

    api_key = os.getenv('WAVESPEED_API_KEY')

    if not api_key:
        print("❌ WAVESPEED_API_KEY não encontrada no .env")
        return

    try:
        # 1. Cria arquivos de teste
        audio_file, image_file = create_test_files()

        # 2. Faz upload dos arquivos
        print("📤 Fazendo upload de arquivos...")
        print()

        uploader = WaveSpeedCompatibleUploader()

        try:
            audio_url = uploader.upload_file_wavespeed_compatible(audio_file)
            print()
        except Exception as e:
            print(f"❌ Falha ao fazer upload do áudio: {e}")
            return

        try:
            image_url = uploader.upload_file_wavespeed_compatible(image_file)
            print()
        except Exception as e:
            print(f"❌ Falha ao fazer upload da imagem: {e}")
            return

        print("✅ Uploads concluídos!")
        print(f"   Áudio: {audio_url}")
        print(f"   Imagem: {image_url}")
        print()

        # 3. Testa submissão para WaveSpeed
        print("🔄 Submetendo para WaveSpeed...")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "audio": audio_url,
            "image": image_url,
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

        if response.status_code != 200:
            print(f"❌ Erro na submissão: {response.text}")
            return

        data = response.json()

        if data.get("code") != 200:
            print(f"❌ API retornou erro: {data}")
            return

        request_id = data.get("data", {}).get("id")
        print(f"   ✅ Tarefa submetida: {request_id}")
        print()

        # 4. Aguarda e verifica resultado
        print("⏳ Aguardando 20 segundos antes de verificar...")
        time.sleep(20)

        print("🔍 Verificando status...")

        result_response = requests.get(
            f"https://api.wavespeed.ai/api/v3/predictions/{request_id}/result",
            headers=headers,
            timeout=30
        )

        result_data = result_response.json()
        status = result_data.get("data", {}).get("status")

        print(f"   Status: {status}")
        print()

        if status == "failed":
            error = result_data.get("data", {}).get("error", "Erro desconhecido")
            print("❌ TAREFA FALHOU!")
            print(f"   Erro: {error}")
            print()

            # Analisa o erro
            if "403" in error or "Forbidden" in error:
                print("⚠️  DIAGNÓSTICO:")
                print("   O serviço de upload usado ainda está bloqueado pela WaveSpeed")
                print()
                print("   URLs testadas:")
                print(f"   - Áudio: {audio_url}")
                print(f"   - Imagem: {image_url}")
                print()
                print("   Soluções:")
                print("   1. Tente usar um serviço diferente de upload")
                print("   2. Considere usar AWS S3 + CloudFront (100% compatível)")
                print("   3. Verifique se as URLs são acessíveis publicamente")
            else:
                print("   Resposta completa:")
                print(result_data)

        elif status == "completed":
            output_url = result_data.get("data", {}).get("outputs", [None])[0]
            print("🎉 SUCESSO COMPLETO!")
            print(f"   Vídeo gerado: {output_url}")
            print()
            print("✅ Todo o pipeline está funcionando:")
            print("   1. ✅ Upload de arquivos")
            print("   2. ✅ Submissão para WaveSpeed")
            print("   3. ✅ Processamento de vídeo")
            print("   4. ✅ Geração completa")
            print()
            print("🚀 O sistema está pronto para uso!")

        elif status == "processing":
            print("⏳ Tarefa ainda processando...")
            print("   A API está aceitando as URLs!")
            print("   Isso é um bom sinal.")
            print()
            print("   Continue fazendo polls ou aguarde mais tempo.")
            print("   (Vídeos podem levar 2-5 minutos)")

        else:
            print(f"⚠️  Status desconhecido: {status}")
            print("   Resposta completa:")
            print(result_data)

        # Limpeza
        print()
        print("🧹 Limpando arquivos de teste...")
        audio_file.unlink(missing_ok=True)
        image_file.unlink(missing_ok=True)
        print("✅ Limpeza concluída")

    except Exception as e:
        print(f"❌ Erro: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_wavespeed_complete_pipeline()
