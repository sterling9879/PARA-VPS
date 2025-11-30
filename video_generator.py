"""
Módulo de geração de vídeo com lip-sync usando WaveSpeed Wan 2.2 API
"""
import time
import requests
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import Config
from utils import get_logger, retry_with_backoff, select_random_image

logger = get_logger(__name__)

class WaveSpeedClient:
    """Cliente para WaveSpeed API"""

    BASE_URL = "https://api.wavespeed.ai/api/v3"

    def __init__(self, api_key: str):
        """
        Inicializa o cliente WaveSpeed

        Args:
            api_key: Chave da API WaveSpeed
        """
        self.api_key = api_key
        self.session = requests.Session()
        logger.info("WaveSpeedClient inicializado")

    def _headers(self) -> dict:
        """Retorna headers para requisições"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    @retry_with_backoff(max_retries=3, base_delay=2.0)
    def submit_task(self, audio_url: str, image_url: str, resolution: str = "480p") -> str:
        """
        Submete tarefa de geração de vídeo

        Args:
            audio_url: URL pública do áudio
            image_url: URL pública da imagem
            resolution: Resolução do vídeo (480p, 720p, 1080p)

        Returns:
            request_id da tarefa

        Raises:
            Exception: Se a submissão falhar
        """
        try:
            endpoint = f"{self.BASE_URL}/wavespeed-ai/wan-2.2/speech-to-video"

            payload = {
                "audio": audio_url,
                "image": image_url,
                "prompt": "",
                "resolution": resolution,
                "seed": -1
            }

            logger.info(f"Submetendo tarefa: {endpoint}")

            response = self.session.post(
                endpoint,
                headers=self._headers(),
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            if data.get("code") != 200:
                raise Exception(f"API retornou código {data.get('code')}: {data.get('message')}")

            request_id = data.get("data", {}).get("id")

            if not request_id:
                raise Exception("Resposta da API sem request_id")

            logger.info(f"Tarefa submetida com sucesso: {request_id}")

            return request_id

        except requests.HTTPError as e:
            if e.response.status_code == 429:
                logger.warning("Rate limit atingido")
                raise Exception("Rate limit atingido. Aguarde alguns segundos.")
            logger.error(f"Erro HTTP ao submeter tarefa: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao submeter tarefa: {e}")
            raise

    def poll_result(self, request_id: str, poll_interval: float = None, poll_timeout: float = None) -> dict:
        """
        Faz polling até obter resultado da tarefa

        Args:
            request_id: ID da tarefa
            poll_interval: Intervalo entre polls em segundos
            poll_timeout: Timeout total em segundos

        Returns:
            Dict com dados do resultado

        Raises:
            Exception: Se polling falhar ou timeout
        """
        if poll_interval is None:
            poll_interval = Config.POLL_INTERVAL

        if poll_timeout is None:
            poll_timeout = Config.POLL_TIMEOUT

        endpoint = f"{self.BASE_URL}/predictions/{request_id}/result"
        start_time = time.time()

        logger.info(f"Iniciando polling para tarefa {request_id}")

        # Aguarda 15 segundos antes do primeiro poll (API precisa de tempo para processar)
        logger.info("Aguardando 15s antes do primeiro poll (API processando)...")
        time.sleep(15)

        poll_count = 0
        max_connection_errors = 5

        while True:
            poll_count += 1

            try:
                logger.info(f"Poll #{poll_count} para tarefa {request_id}...")

                response = self.session.get(
                    endpoint,
                    headers=self._headers(),
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()
                status = data.get("data", {}).get("status")

                logger.info(f"Status da tarefa {request_id}: {status}")

                if status == "completed":
                    logger.info(f"✅ Tarefa {request_id} concluída com sucesso")
                    return data["data"]

                elif status == "failed":
                    error_msg = data.get("data", {}).get("error", "Erro desconhecido")
                    raise Exception(f"Processamento falhou na API: {error_msg}")

                # Verifica timeout
                elapsed = time.time() - start_time
                if elapsed > poll_timeout:
                    raise Exception(f"Timeout após {poll_timeout}s aguardando resultado")

                # Aguarda antes do próximo poll
                logger.info(f"Aguardando {poll_interval}s antes do próximo poll...")
                time.sleep(poll_interval)

            except requests.exceptions.ConnectionError as e:
                logger.warning(f"⚠️  Erro de conexão no poll #{poll_count}: {e}")

                if poll_count >= max_connection_errors:
                    raise Exception(
                        f"Muitos erros de conexão ({max_connection_errors}). "
                        "A API WaveSpeed pode estar sobrecarregada ou instável."
                    )

                # Aguarda mais tempo antes de tentar novamente
                logger.info("Aguardando 10s devido a erro de conexão...")
                time.sleep(10)
                continue

            except requests.HTTPError as e:
                if e.response.status_code == 429:
                    logger.warning("Rate limit no polling, aguardando 30s...")
                    time.sleep(30)
                    continue
                elif e.response.status_code >= 500:
                    logger.warning(f"Erro do servidor ({e.response.status_code}), aguardando 15s...")
                    time.sleep(15)
                    continue
                else:
                    raise

            except Exception as e:
                logger.error(f"Erro inesperado no polling: {type(e).__name__}: {e}")
                raise

    def process_video(
        self,
        audio_url: str,
        image_url: str,
        resolution: str = "480p"
    ) -> str:
        """
        Pipeline completo: submete + aguarda + retorna URL do vídeo

        Args:
            audio_url: URL pública do áudio
            image_url: URL pública da imagem
            resolution: Resolução do vídeo

        Returns:
            URL do vídeo gerado

        Raises:
            Exception: Se o processamento falhar
        """
        request_id = self.submit_task(audio_url, image_url, resolution)
        result = self.poll_result(request_id)

        outputs = result.get("outputs", [])
        if not outputs:
            raise Exception("Nenhum output retornado pela API")

        return outputs[0]

class FileUploader:
    """Classe para upload de arquivos para serviços temporários"""

    @staticmethod
    def upload_to_fileio(file_path: Path) -> str:
        """
        Faz upload de arquivo para file.io (14 dias de retenção)

        Args:
            file_path: Caminho do arquivo

        Returns:
            URL pública do arquivo

        Raises:
            Exception: Se o upload falhar
        """
        try:
            logger.info(f"Tentando upload para file.io...")

            with open(file_path, 'rb') as f:
                response = requests.post(
                    'https://file.io',
                    files={'file': f},
                    timeout=120
                )

            response.raise_for_status()
            data = response.json()

            if data.get('success'):
                url = data['link']
                logger.info(f"✅ Upload file.io concluído: {url}")
                return url
            else:
                raise Exception(f"file.io retornou erro: {data}")

        except Exception as e:
            logger.error(f"❌ file.io falhou: {e}")
            raise

    @staticmethod
    def upload_to_tmpfiles(file_path: Path) -> str:
        """
        Faz upload de arquivo para tmpfiles.org (1 hora de retenção)

        Args:
            file_path: Caminho do arquivo

        Returns:
            URL pública do arquivo

        Raises:
            Exception: Se o upload falhar
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

            if data.get('status') == 'success':
                # tmpfiles retorna URL no formato tmpfiles.org/xxx
                # Precisa converter para tmpfiles.org/dl/xxx para download direto
                url = data['data']['url']
                url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
                logger.info(f"✅ Upload tmpfiles.org concluído: {url}")
                return url
            else:
                raise Exception(f"tmpfiles.org retornou erro: {data}")

        except Exception as e:
            logger.error(f"❌ tmpfiles.org falhou: {e}")
            raise

    @staticmethod
    def upload_to_catbox(file_path: Path) -> str:
        """
        Faz upload de arquivo para catbox.moe (permanente, até 200MB)

        Args:
            file_path: Caminho do arquivo

        Returns:
            URL pública do arquivo

        Raises:
            Exception: Se o upload falhar
        """
        try:
            logger.info(f"Tentando upload para catbox.moe...")

            with open(file_path, 'rb') as f:
                response = requests.post(
                    'https://catbox.moe/user/api.php',
                    data={'reqtype': 'fileupload'},
                    files={'fileToUpload': f},
                    timeout=120
                )

            response.raise_for_status()

            # Catbox retorna diretamente a URL
            url = response.text.strip()

            if url.startswith('http'):
                logger.info(f"✅ Upload catbox.moe concluído: {url}")
                return url
            else:
                raise Exception(f"catbox.moe retornou resposta inválida: {url}")

        except Exception as e:
            logger.error(f"❌ catbox.moe falhou: {e}")
            raise

    @staticmethod
    def upload_to_0x0(file_path: Path) -> str:
        """
        Faz upload de arquivo para 0x0.st (365 dias, até 512MB)

        Args:
            file_path: Caminho do arquivo

        Returns:
            URL pública do arquivo

        Raises:
            Exception: Se o upload falhar
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

            url = response.text.strip()
            logger.info(f"✅ Upload 0x0.st concluído: {url}")
            return url

        except Exception as e:
            logger.error(f"❌ 0x0.st falhou: {e}")
            raise

    @staticmethod
    def upload_file(file_path: Path) -> str:
        """
        Faz upload de arquivo tentando múltiplos serviços com fallback automático

        Ordem de tentativa:
        1. catbox.moe (permanente, mais confiável)
        2. file.io (14 dias)
        3. tmpfiles.org (1 hora)
        4. 0x0.st (365 dias)

        Args:
            file_path: Caminho do arquivo

        Returns:
            URL pública do arquivo

        Raises:
            Exception: Se todos os serviços falharem
        """
        logger.info(f"📤 Iniciando upload de {file_path.name}...")

        # Lista de serviços para tentar (em ordem de preferência)
        upload_services = [
            ('catbox.moe', FileUploader.upload_to_catbox),
            ('file.io', FileUploader.upload_to_fileio),
            ('tmpfiles.org', FileUploader.upload_to_tmpfiles),
            ('0x0.st', FileUploader.upload_to_0x0),
        ]

        errors = []

        for service_name, upload_func in upload_services:
            try:
                logger.info(f"🔄 Tentando {service_name}...")
                url = upload_func(file_path)
                logger.info(f"✅ Upload bem-sucedido via {service_name}")
                return url

            except Exception as e:
                error_msg = f"{service_name}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"⚠️  {service_name} falhou, tentando próximo serviço...")
                continue

        # Se chegou aqui, todos falharam
        error_details = "\n".join(f"  - {err}" for err in errors)
        raise Exception(
            f"Falha ao fazer upload de {file_path.name}. "
            f"Todos os serviços falharam:\n{error_details}"
        )

class VideoGenerator:
    """Gera vídeos com lip-sync usando WaveSpeed"""

    def __init__(self):
        """Inicializa o gerador de vídeo"""
        self.client = WaveSpeedClient(Config.WAVESPEED_API_KEY)
        self.uploader = FileUploader()
        logger.info("VideoGenerator inicializado")

    def generate_videos_batch(
        self,
        audios: List[Dict],
        image_paths: List[Path],
        output_dir: Path,
        progress_callback=None,
        max_workers: int = 3
    ) -> List[Dict]:
        """
        Gera múltiplos vídeos com lip-sync

        Args:
            audios: Lista de dicts com informações dos áudios
                    [{'audio_number': 1, 'audio_path': Path('audio_1.mp3'), ...}, ...]
            image_paths: Lista de Paths das imagens disponíveis
            output_dir: Diretório para salvar vídeos
            progress_callback: Função de callback para progresso
            max_workers: Número máximo de workers paralelos

        Returns:
            Lista de dicts com informações dos vídeos gerados
            [
                {
                    'video_number': 1,
                    'audio_path': Path('audio_1.mp3'),
                    'image_path': Path('image_1.jpg'),
                    'video_path': Path('video_1.mp4')
                },
                ...
            ]
        """
        logger.info(f"Iniciando geração de {len(audios)} vídeos")

        # Cria diretórios
        video_dir = output_dir / 'videos'
        video_dir.mkdir(parents=True, exist_ok=True)

        images_dir = output_dir / 'images'
        images_dir.mkdir(parents=True, exist_ok=True)

        # Copia imagens para diretório do job
        image_pool = []
        for idx, img_path in enumerate(image_paths, start=1):
            dest = images_dir / f"image_{idx}{Path(img_path).suffix}"
            if not dest.exists():
                import shutil
                shutil.copy2(img_path, dest)
            image_pool.append(dest)

        results = []
        used_images = []

        def generate_single_video(audio_data: Dict) -> Dict:
            """Gera um único vídeo"""
            video_number = audio_data['audio_number']
            audio_path = audio_data['audio_path']

            if not audio_path or not audio_path.exists():
                raise Exception(f"Áudio não encontrado: {audio_path}")

            # Seleciona imagem aleatória (evita repetições consecutivas)
            image_path = select_random_image(image_pool, used_images)
            used_images.append(image_path)

            if progress_callback:
                progress_callback(f"Gerando vídeo {video_number}/{len(audios)} (lip-sync)...")

            logger.info(f"Gerando vídeo {video_number}: áudio={audio_path.name}, imagem={image_path.name}")

            # Upload de arquivos (usando serviços compatíveis com WaveSpeed)
            from wavespeed_uploader import WaveSpeedCompatibleUploader

            audio_url = WaveSpeedCompatibleUploader.upload_file_wavespeed_compatible(audio_path)
            image_url = WaveSpeedCompatibleUploader.upload_file_wavespeed_compatible(image_path)

            # Gera vídeo
            video_url = self.client.process_video(
                audio_url=audio_url,
                image_url=image_url,
                resolution=Config.DEFAULT_RESOLUTION
            )

            # Baixa vídeo gerado
            video_path = video_dir / f'video_{video_number}.mp4'

            logger.info(f"Baixando vídeo {video_number} de {video_url}...")

            response = requests.get(video_url, stream=True, timeout=120)
            response.raise_for_status()

            with open(video_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    f.write(chunk)

            logger.info(f"Vídeo {video_number} salvo em: {video_path}")

            return {
                'video_number': video_number,
                'audio_path': audio_path,
                'image_path': image_path,
                'video_path': video_path
            }

        # Processa em paralelo (WaveSpeed suporta múltiplas requisições simultâneas)
        from concurrent.futures import ThreadPoolExecutor, as_completed

        logger.info(f"🚀 Enviando {len(audios)} vídeos para a fila do WaveSpeed em paralelo...")

        # Notifica que todos os vídeos foram enviados para a fila
        if progress_callback:
            progress_callback(f"🎬 {len(audios)} vídeos na fila do WaveSpeed (processando em paralelo)...")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submete todos os vídeos para processamento paralelo
            futures = {
                executor.submit(generate_single_video, audio_data): audio_data
                for audio_data in audios
            }

            # Aguarda conclusão de cada vídeo
            for future in as_completed(futures):
                audio_data = futures[future]
                try:
                    result = future.result()
                    results.append(result)

                    # Atualiza progresso com contador
                    completed = len(results)
                    remaining = len(audios) - completed
                    logger.info(f"✅ Vídeo {result['video_number']} concluído ({completed}/{len(audios)})")

                    if progress_callback:
                        progress_callback(f"✅ Vídeo {completed}/{len(audios)} concluído | {remaining} em processamento...")

                except Exception as e:
                    logger.error(f"❌ Erro ao gerar vídeo {audio_data['audio_number']}: {e}")
                    results.append({
                        'video_number': audio_data['audio_number'],
                        'audio_path': audio_data['audio_path'],
                        'image_path': None,
                        'video_path': None,
                        'error': str(e)
                    })

                    # Atualiza progresso mesmo com erro
                    completed = len(results)
                    remaining = len(audios) - completed
                    if progress_callback:
                        progress_callback(f"⚠️ Vídeo {completed}/{len(audios)} processado (com erro) | {remaining} em processamento...")

        # Ordena resultados por número
        results.sort(key=lambda x: x['video_number'])

        logger.info(f"Geração de vídeos concluída: {len(results)} vídeos")

        return results

def test_video_generator():
    """Função de teste do gerador de vídeo"""
    print(f"\n{'='*60}")
    print(f"TESTE DO VIDEO GENERATOR")
    print(f"{'='*60}\n")
    print("Para testar o VideoGenerator, você precisa de:")
    print("1. Arquivos de áudio válidos")
    print("2. Imagens válidas")
    print("3. Chave API do WaveSpeed configurada")
    print("\nUse este módulo integrado com audio_generator.py")

if __name__ == "__main__":
    test_video_generator()
