"""
Uploader usando serviços compatíveis com WaveSpeed
Usa 0x0.st como primário e tmpfiles.org como fallback
"""
import requests
from pathlib import Path
from utils import get_logger

logger = get_logger(__name__)

class WaveSpeedCompatibleUploader:
    """Upload de arquivos para serviços compatíveis com WaveSpeed"""

    @staticmethod
    def upload_to_0x0st(file_path: Path) -> str:
        """
        Faz upload para 0x0.st (compatível com WaveSpeed)
        Retorna URL como texto puro
        """
        try:
            logger.info(f"Tentando upload para 0x0.st...")

            with open(file_path, 'rb') as f:
                response = requests.post(
                    'https://0x0.st',
                    files={'file': f},
                    timeout=120
                )

            response.raise_for_status()

            # 0x0.st retorna a URL como texto puro
            url = response.text.strip()

            if url.startswith('http'):
                logger.info(f"✅ Upload 0x0.st concluído: {url}")
                return url
            else:
                raise Exception(f"0x0.st retornou resposta inválida: {url}")

        except Exception as e:
            logger.error(f"❌ 0x0.st falhou: {e}")
            raise

    @staticmethod
    def upload_to_tmpfiles(file_path: Path) -> str:
        """
        Faz upload para tmpfiles.org (fallback compatível com WaveSpeed)
        Retorna JSON e requer conversão de URL
        """
        try:
            logger.info(f"Tentando upload para tmpfiles.org...")

            with open(file_path, 'rb') as f:
                response = requests.post(
                    'https://tmpfiles.org/api/v1/upload',
                    files={'file': f},
                    timeout=120
                )

            response.raise_for_status()
            data = response.json()

            # Extrai URL do JSON (formato: data.url)
            if data.get('status') == 'success' and 'data' in data and 'url' in data['data']:
                url = data['data']['url']

                # Converte URL de tmpfiles.org/123 para tmpfiles.org/dl/123
                if 'tmpfiles.org/' in url:
                    url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')

                logger.info(f"✅ Upload tmpfiles.org concluído: {url}")
                return url
            else:
                raise Exception(f"tmpfiles.org retornou formato inválido: {data}")

        except Exception as e:
            logger.error(f"❌ tmpfiles.org falhou: {e}")
            raise

    @staticmethod
    def upload_file_wavespeed_compatible(file_path: Path) -> str:
        """
        Faz upload para serviços compatíveis com WaveSpeed
        Usa 0x0.st como primário e tmpfiles.org como fallback

        Returns:
            URL pública acessível pela WaveSpeed
        """
        logger.info(f"📤 Upload compatível WaveSpeed: {file_path.name}...")

        # Serviços compatíveis testados com WaveSpeed
        upload_services = [
            {
                "name": "0x0.st",
                "upload_func": WaveSpeedCompatibleUploader.upload_to_0x0st,
            },
            {
                "name": "tmpfiles.org",
                "upload_func": WaveSpeedCompatibleUploader.upload_to_tmpfiles,
            },
        ]

        errors = []

        for service in upload_services:
            service_name = service["name"]
            upload_func = service["upload_func"]

            try:
                logger.info(f"🔄 Tentando {service_name}...")
                url = upload_func(file_path)
                logger.info(f"✅ Upload bem-sucedido via {service_name}")

                # Testa se a URL é acessível
                test_response = requests.head(url, timeout=10, allow_redirects=True)
                if test_response.status_code == 200:
                    logger.info(f"✅ URL verificada e acessível: {url}")
                    return url
                else:
                    logger.warning(f"⚠️  URL retornou status {test_response.status_code}")
                    continue

            except Exception as e:
                error_msg = f"{service_name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"⚠️  {service_name} falhou, tentando próximo...")
                continue

        # Se todos falharam
        error_details = "\n".join(f"  - {err}" for err in errors)
        raise Exception(
            f"Falha ao fazer upload de {file_path.name} para serviços compatíveis. "
            f"Todos os serviços falharam:\n{error_details}"
        )
