"""
Script de teste para validar serviços de upload de arquivos
"""
import os
from pathlib import Path
from video_generator import FileUploader
import tempfile

def create_test_file():
    """Cria um arquivo de teste pequeno"""
    test_content = b"Este eh um arquivo de teste para validar os uploads.\n" * 100

    # Cria arquivo temporário
    temp_file = Path(tempfile.gettempdir()) / "test_upload.txt"
    temp_file.write_bytes(test_content)

    return temp_file

def test_uploads():
    """Testa todos os serviços de upload"""

    print("="*60)
    print("🧪 TESTE DE SERVIÇOS DE UPLOAD")
    print("="*60)
    print()

    # Cria arquivo de teste
    print("📝 Criando arquivo de teste...")
    test_file = create_test_file()
    file_size = test_file.stat().st_size
    print(f"✅ Arquivo criado: {test_file}")
    print(f"   Tamanho: {file_size:,} bytes (~{file_size/1024:.1f} KB)")
    print()

    uploader = FileUploader()

    # Lista de serviços para testar
    services = [
        ("catbox.moe", uploader.upload_to_catbox),
        ("file.io", uploader.upload_to_fileio),
        ("tmpfiles.org", uploader.upload_to_tmpfiles),
        ("0x0.st", uploader.upload_to_0x0),
    ]

    results = []

    for service_name, upload_func in services:
        print(f"🔄 Testando {service_name}...")
        try:
            url = upload_func(test_file)
            print(f"   ✅ SUCESSO: {url}")
            results.append((service_name, "✅ Funcionando", url))
        except Exception as e:
            print(f"   ❌ FALHOU: {e}")
            results.append((service_name, "❌ Falhou", str(e)))
        print()

    # Testa o método com fallback automático
    print("🔄 Testando método com fallback automático...")
    try:
        url = uploader.upload_file(test_file)
        print(f"   ✅ SUCESSO (fallback automático): {url}")
        results.append(("Fallback Auto", "✅ Funcionando", url))
    except Exception as e:
        print(f"   ❌ FALHOU: {e}")
        results.append(("Fallback Auto", "❌ Falhou", str(e)))
    print()

    # Resumo
    print("="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)

    working_count = sum(1 for _, status, _ in results if "✅" in status)

    for service, status, info in results:
        print(f"{service:20s} {status}")
        if "❌" in status:
            print(f"{'':20s}    Erro: {info[:50]}...")

    print("="*60)
    print(f"\n📈 Resultado: {working_count}/{len(results)} serviços funcionando")

    # Limpeza
    print(f"\n🧹 Limpando arquivo de teste...")
    test_file.unlink(missing_ok=True)
    print("✅ Arquivo removido")

    if working_count > 0:
        print("\n🎉 Pelo menos um serviço está funcionando!")
        print("   O sistema usará fallback automático se algum falhar.")
    else:
        print("\n⚠️  AVISO: Nenhum serviço de upload está funcionando!")
        print("   Possíveis causas:")
        print("   - Conexão com internet")
        print("   - Firewall bloqueando")
        print("   - Serviços temporariamente indisponíveis")

if __name__ == "__main__":
    test_uploads()
