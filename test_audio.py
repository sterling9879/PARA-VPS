"""
Script de teste para validar geração de áudio com ElevenLabs
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import ElevenLabs

load_dotenv()

def test_elevenlabs_audio():
    """Testa geração de áudio com ElevenLabs"""

    print("="*60)
    print("🧪 TESTE DE GERAÇÃO DE ÁUDIO - ELEVENLABS")
    print("="*60)
    print()

    # Inicializa cliente
    api_key = os.getenv('ELEVENLABS_API_KEY')

    if not api_key:
        print("❌ ELEVENLABS_API_KEY não encontrada no .env")
        return

    print(f"✅ API Key encontrada: {api_key[:20]}...")
    print()

    try:
        client = ElevenLabs(api_key=api_key)
        print("✅ Cliente ElevenLabs inicializado")
        print()

        # Lista vozes
        print("📋 Buscando vozes disponíveis...")
        voices_response = client.voices.get_all()
        voices = voices_response.voices

        print(f"✅ Encontradas {len(voices)} vozes")
        print()

        # Seleciona primeira voz
        if not voices:
            print("❌ Nenhuma voz disponível")
            return

        first_voice = voices[0]
        print(f"🎤 Usando voz: {first_voice.name} (ID: {first_voice.voice_id})")
        print()

        # Texto de teste
        test_text = "Olá! Este é um teste de geração de áudio com ElevenLabs."
        print(f"📝 Texto: {test_text}")
        print()

        # Gera áudio
        print("🎵 Gerando áudio...")

        audio_data = client.text_to_speech.convert(
            voice_id=first_voice.voice_id,
            text=test_text,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )

        # Salva arquivo de teste
        output_path = Path("test_audio.mp3")

        with open(output_path, 'wb') as f:
            for chunk in audio_data:
                f.write(chunk)

        print(f"✅ Áudio gerado com sucesso!")
        print(f"📁 Salvo em: {output_path.absolute()}")
        print(f"📊 Tamanho: {output_path.stat().st_size / 1024:.2f} KB")
        print()

        print("="*60)
        print("🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print()
        print("✅ A geração de áudio está funcionando corretamente")
        print("✅ Você pode deletar o arquivo test_audio.mp3")

    except Exception as e:
        print("="*60)
        print("❌ ERRO NO TESTE")
        print("="*60)
        print()
        print(f"Erro: {e}")
        print()
        print("Possíveis causas:")
        print("1. API key inválida")
        print("2. Sem créditos na conta ElevenLabs")
        print("3. Versão da biblioteca incompatível")
        print()
        print("Execute: python check_api_keys.py")

if __name__ == "__main__":
    test_elevenlabs_audio()
