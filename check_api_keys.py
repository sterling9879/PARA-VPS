"""
Script para verificar e validar as API keys configuradas
"""
import os
from dotenv import load_dotenv
import requests

# Carrega .env
load_dotenv()

def check_elevenlabs_key():
    """Verifica a API key do ElevenLabs"""
    print("\n🔍 Verificando ElevenLabs API Key...")

    api_key = os.getenv('ELEVENLABS_API_KEY')

    if not api_key:
        print("❌ ELEVENLABS_API_KEY não encontrada no .env")
        return False

    if len(api_key) < 10:
        print(f"❌ ELEVENLABS_API_KEY parece inválida (muito curta): {api_key[:20]}...")
        return False

    # Tenta fazer uma requisição de teste
    try:
        headers = {"xi-api-key": api_key}
        response = requests.get(
            "https://api.elevenlabs.io/v1/voices",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            voices = data.get('voices', [])
            print(f"✅ ElevenLabs API Key VÁLIDA!")
            print(f"   {len(voices)} vozes disponíveis")
            if voices:
                print(f"   Exemplos: {', '.join([v['name'] for v in voices[:3]])}")
            return True
        elif response.status_code == 401:
            print(f"❌ ElevenLabs API Key INVÁLIDA!")
            print(f"   Status: 401 Unauthorized")
            print(f"   Mensagem: {response.json().get('detail', {}).get('message', 'Sem mensagem')}")
            print(f"\n   Sua chave atual (primeiros 20 caracteres): {api_key[:20]}...")
            print(f"\n   Como obter uma chave válida:")
            print(f"   1. Acesse: https://elevenlabs.io")
            print(f"   2. Faça login ou crie uma conta")
            print(f"   3. Vá em: Settings → API Keys")
            print(f"   4. Copie a chave e cole no arquivo .env")
            return False
        else:
            print(f"⚠️  Resposta inesperada da API: {response.status_code}")
            print(f"   {response.text}")
            return False

    except Exception as e:
        print(f"❌ Erro ao verificar ElevenLabs: {e}")
        return False

def check_gemini_key():
    """Verifica a API key do Gemini"""
    print("\n🔍 Verificando Gemini API Key...")

    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print("❌ GEMINI_API_KEY não encontrada no .env")
        return False

    if len(api_key) < 10:
        print(f"❌ GEMINI_API_KEY parece inválida (muito curta): {api_key[:20]}...")
        return False

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        # Tenta listar modelos
        models = genai.list_models()
        model_list = list(models)

        print(f"✅ Gemini API Key VÁLIDA!")
        print(f"   {len(model_list)} modelos disponíveis")
        return True

    except Exception as e:
        print(f"❌ Gemini API Key INVÁLIDA!")
        print(f"   Erro: {e}")
        print(f"\n   Como obter uma chave válida:")
        print(f"   1. Acesse: https://ai.google.dev")
        print(f"   2. Clique em 'Get API Key'")
        print(f"   3. Copie a chave e cole no arquivo .env")
        return False

def check_wavespeed_key():
    """Verifica a API key do WaveSpeed"""
    print("\n🔍 Verificando WaveSpeed API Key...")

    api_key = os.getenv('WAVESPEED_API_KEY')

    if not api_key:
        print("❌ WAVESPEED_API_KEY não encontrada no .env")
        return False

    if len(api_key) < 10:
        print(f"❌ WAVESPEED_API_KEY parece inválida (muito curta): {api_key[:20]}...")
        return False

    print(f"⚠️  WaveSpeed: Verificação básica OK (comprimento adequado)")
    print(f"   A validação completa só ocorre ao processar um vídeo")
    print(f"   Chave configurada (primeiros 20 caracteres): {api_key[:20]}...")
    return True

def main():
    """Verifica todas as API keys"""
    print("="*60)
    print("🔐 VERIFICAÇÃO DE API KEYS")
    print("="*60)

    # Verifica se .env existe
    if not os.path.exists('.env'):
        print("\n❌ Arquivo .env não encontrado!")
        print("   Execute: copy .env.example .env (Windows)")
        print("   Execute: cp .env.example .env (Linux/Mac)")
        return

    results = []

    # Verifica cada API
    results.append(("ElevenLabs", check_elevenlabs_key()))
    results.append(("Gemini", check_gemini_key()))
    results.append(("WaveSpeed", check_wavespeed_key()))

    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)

    all_valid = True
    for name, is_valid in results:
        status = "✅ VÁLIDA" if is_valid else "❌ INVÁLIDA"
        print(f"{name:20s} {status}")
        if not is_valid:
            all_valid = False

    print("="*60)

    if all_valid:
        print("\n🎉 Todas as API keys estão configuradas corretamente!")
        print("\n▶️  Você pode iniciar a aplicação: python app.py")
    else:
        print("\n⚠️  Algumas API keys precisam ser corrigidas.")
        print("\n📝 Para editar o arquivo .env:")
        print("   Windows: notepad .env")
        print("   Linux/Mac: nano .env")
        print("\n   Depois de editar, execute este script novamente para validar.")

if __name__ == "__main__":
    main()
