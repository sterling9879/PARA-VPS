"""
Script de teste para validar a configuração do sistema
"""
import sys
from pathlib import Path

def test_imports():
    """Testa se todas as dependências estão instaladas"""
    print("🔍 Testando imports...")

    required_modules = [
        ('gradio', 'Gradio'),
        ('dotenv', 'python-dotenv'),
        ('requests', 'requests'),
        ('google.generativeai', 'google-generativeai'),
        ('elevenlabs', 'elevenlabs'),
        ('PIL', 'Pillow'),
    ]

    errors = []

    for module, package in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NÃO INSTALADO")
            errors.append(package)

    if errors:
        print(f"\n⚠️  Instale os pacotes faltantes:")
        print(f"pip install {' '.join(errors)}")
        return False

    print("\n✅ Todos os módulos Python estão instalados!")
    return True

def test_ffmpeg():
    """Testa se FFmpeg está instalado"""
    print("\n🔍 Testando FFmpeg...")

    import subprocess

    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"  ✅ {version}")
            return True
        else:
            print("  ❌ FFmpeg não está funcionando")
            return False

    except FileNotFoundError:
        print("  ❌ FFmpeg não encontrado")
        print("\n  Instale FFmpeg:")
        print("    Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("    macOS: brew install ffmpeg")
        print("    Windows: https://ffmpeg.org/download.html")
        return False

def test_config():
    """Testa se as configurações estão corretas"""
    print("\n🔍 Testando configurações...")

    try:
        from config import Config

        print(f"  ✅ Arquivo de configuração carregado")

        # Verifica se as chaves estão presentes
        if Config.ELEVENLABS_API_KEY and len(Config.ELEVENLABS_API_KEY) > 10:
            print(f"  ✅ ElevenLabs API Key configurada")
        else:
            print(f"  ⚠️  ElevenLabs API Key não configurada ou inválida")

        if Config.GEMINI_API_KEY and len(Config.GEMINI_API_KEY) > 10:
            print(f"  ✅ Gemini API Key configurada")
        else:
            print(f"  ⚠️  Gemini API Key não configurada ou inválida")

        if Config.WAVESPEED_API_KEY and len(Config.WAVESPEED_API_KEY) > 10:
            print(f"  ✅ WaveSpeed API Key configurada")
        else:
            print(f"  ⚠️  WaveSpeed API Key não configurada ou inválida")

        # Verifica diretório temp
        if Config.TEMP_FOLDER.exists():
            print(f"  ✅ Diretório temporário: {Config.TEMP_FOLDER}")
        else:
            Config.TEMP_FOLDER.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Diretório temporário criado: {Config.TEMP_FOLDER}")

        return True

    except Exception as e:
        print(f"  ❌ Erro ao carregar configurações: {e}")
        return False

def test_modules():
    """Testa módulos do sistema"""
    print("\n🔍 Testando módulos do sistema...")

    try:
        from text_processor import TextProcessor
        print(f"  ✅ TextProcessor")
    except Exception as e:
        print(f"  ❌ TextProcessor: {e}")
        return False

    try:
        from audio_generator import AudioGenerator
        print(f"  ✅ AudioGenerator")
    except Exception as e:
        print(f"  ❌ AudioGenerator: {e}")
        return False

    try:
        from video_generator import VideoGenerator
        print(f"  ✅ VideoGenerator")
    except Exception as e:
        print(f"  ❌ VideoGenerator: {e}")
        return False

    try:
        from video_concatenator import VideoConcatenator
        print(f"  ✅ VideoConcatenator")
    except Exception as e:
        print(f"  ❌ VideoConcatenator: {e}")
        return False

    try:
        from job_manager import JobManager
        print(f"  ✅ JobManager")
    except Exception as e:
        print(f"  ❌ JobManager: {e}")
        return False

    return True

def main():
    """Executa todos os testes"""
    print("="*60)
    print("🧪 TESTE DE CONFIGURAÇÃO DO SISTEMA")
    print("="*60)

    results = []

    results.append(("Dependências Python", test_imports()))
    results.append(("FFmpeg", test_ffmpeg()))
    results.append(("Configurações", test_config()))
    results.append(("Módulos do Sistema", test_modules()))

    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)

    all_passed = True
    for name, passed in results:
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{name:30s} {status}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\n🎉 Sistema configurado corretamente!")
        print("\n▶️  Próximo passo: python app.py")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Corrija os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
