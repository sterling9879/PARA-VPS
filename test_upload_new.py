"""
Teste rápido do novo sistema de upload (0x0.st + tmpfiles.org)
"""
import tempfile
from pathlib import Path

# Simula o upload sem dependências extras
def test_upload_simple():
    print("=" * 60)
    print("🧪 TESTE DE UPLOAD - 0x0.st + tmpfiles.org")
    print("=" * 60)
    print()

    # Importa o uploader
    try:
        from wavespeed_uploader import WaveSpeedCompatibleUploader
        print("✅ Módulo wavespeed_uploader importado com sucesso")
        print()
    except Exception as e:
        print(f"❌ Erro ao importar: {e}")
        return

    # Cria um arquivo de teste pequeno
    print("📝 Criando arquivo de teste...")
    test_data = b'Test file content for upload verification'
    test_file = Path(tempfile.gettempdir()) / "upload_test.txt"
    test_file.write_bytes(test_data)
    print(f"   ✅ Arquivo criado: {test_file} ({len(test_data)} bytes)")
    print()

    # Testa upload
    try:
        print("📤 Testando upload com novo sistema...")
        print()

        uploader = WaveSpeedCompatibleUploader()
        url = uploader.upload_file_wavespeed_compatible(test_file)

        print()
        print("=" * 60)
        print("✅ UPLOAD BEM-SUCEDIDO!")
        print("=" * 60)
        print(f"URL: {url}")
        print()

        # Verifica qual serviço foi usado
        if '0x0.st' in url:
            print("🎯 Serviço usado: 0x0.st (primário)")
        elif 'tmpfiles.org' in url:
            print("🎯 Serviço usado: tmpfiles.org (fallback)")
        else:
            print("⚠️  Serviço desconhecido")

        print()
        print("🚀 O novo sistema de upload está funcionando!")

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERRO NO UPLOAD")
        print("=" * 60)
        print(f"Erro: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Limpeza
        print()
        print("🧹 Limpando arquivo de teste...")
        test_file.unlink(missing_ok=True)
        print("✅ Limpeza concluída")

if __name__ == "__main__":
    test_upload_simple()
