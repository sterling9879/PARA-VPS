"""
Gerenciador de Jobs - Orquestra todo o pipeline de geração de vídeos
"""
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Callable, Optional
from enum import Enum

from config import Config
from utils import get_logger, validate_text, validate_images, estimate_cost, estimate_time
from text_processor import TextProcessor
from audio_generator import AudioGenerator
from video_generator import VideoGenerator
from video_concatenator import VideoConcatenator

logger = get_logger(__name__)

class JobStatus(Enum):
    """Status possíveis de um job"""
    CREATED = "created"
    PROCESSING_TEXT = "processing_text"
    GENERATING_AUDIO = "generating_audio"
    GENERATING_VIDEO = "generating_video"
    CONCATENATING = "concatenating"
    COMPLETED = "completed"
    FAILED = "failed"

class Job:
    """Representa um job de geração de vídeo"""

    def __init__(self, job_id: str, input_text: str, voice_name: str, image_paths: List[str], model_id: str = "eleven_multilingual_v3", skip_formatting: bool = False):
        """
        Inicializa um novo job

        Args:
            job_id: ID único do job
            input_text: Texto completo de entrada
            voice_name: Nome da voz ElevenLabs
            image_paths: Lista de caminhos das imagens
            model_id: Modelo ElevenLabs a usar
            skip_formatting: Se True, pula a formatação do Gemini
        """
        self.job_id = job_id
        self.input_text = input_text
        self.voice_name = voice_name
        self.model_id = model_id
        self.image_paths = [Path(p) for p in image_paths]
        self.skip_formatting = skip_formatting

        self.status = JobStatus.CREATED
        self.created_at = datetime.now()
        self.completed_at = None
        self.error = None

        # Diretório do job
        self.job_dir = Config.TEMP_FOLDER / f'job_{job_id}'
        self.job_dir.mkdir(parents=True, exist_ok=True)

        # Resultados de cada etapa
        self.formatted_texts = []
        self.audios = []
        self.videos = []
        self.final_video_path = None

        # Progresso
        self.progress_message = "Job criado"
        self.progress_percent = 0

        logger.info(f"Job {job_id} criado (skip_formatting={skip_formatting})")

    def save_state(self):
        """Salva estado atual do job em JSON"""
        state_file = self.job_dir / 'state.json'

        state = {
            'job_id': self.job_id,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error': self.error,
            'voice_name': self.voice_name,
            'progress_message': self.progress_message,
            'progress_percent': self.progress_percent,
            'final_video_path': str(self.final_video_path) if self.final_video_path else None
        }

        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)

        logger.debug(f"Estado do job {self.job_id} salvo")

    def update_progress(self, message: str, percent: int):
        """
        Atualiza progresso do job

        Args:
            message: Mensagem de progresso
            percent: Percentual de conclusão (0-100)
        """
        self.progress_message = message
        self.progress_percent = min(100, max(0, percent))
        self.save_state()
        logger.info(f"Job {self.job_id}: {message} ({percent}%)")

    def mark_completed(self, final_video_path: Path):
        """
        Marca job como concluído

        Args:
            final_video_path: Caminho do vídeo final
        """
        self.status = JobStatus.COMPLETED
        self.completed_at = datetime.now()
        self.final_video_path = final_video_path
        self.update_progress("Concluído com sucesso!", 100)
        logger.info(f"Job {self.job_id} concluído: {final_video_path}")

    def mark_failed(self, error: str):
        """
        Marca job como falho

        Args:
            error: Mensagem de erro
        """
        self.status = JobStatus.FAILED
        self.completed_at = datetime.now()
        self.error = error
        self.save_state()
        logger.error(f"Job {self.job_id} falhou: {error}")

class JobManager:
    """Gerencia a execução de jobs de geração de vídeo"""

    def __init__(self, audio_provider: str = None):
        """
        Inicializa o gerenciador de jobs

        Args:
            audio_provider: 'elevenlabs' ou 'minimax' (padrão: config)
        """
        self.text_processor = TextProcessor()
        self.audio_generator = AudioGenerator(provider=audio_provider)
        self.video_generator = VideoGenerator()
        self.video_concatenator = VideoConcatenator()

        logger.info(f"JobManager inicializado (audio: {self.audio_generator.provider})")

    def create_job(
        self,
        input_text: str,
        voice_name: str,
        image_paths: List[str],
        model_id: str = "eleven_multilingual_v3",
        skip_formatting: bool = False
    ) -> tuple[Optional[Job], Optional[str]]:
        """
        Cria um novo job após validações

        Args:
            input_text: Texto completo de entrada
            voice_name: Nome da voz ElevenLabs
            image_paths: Lista de caminhos das imagens
            model_id: Modelo ElevenLabs a usar
            skip_formatting: Se True, pula a formatação do Gemini (texto já formatado)

        Returns:
            (Job, erro) - Job criado ou None com mensagem de erro
        """
        # Valida texto
        valid, error = validate_text(input_text)
        if not valid:
            return None, error

        # Valida imagens
        valid, error = validate_images(image_paths)
        if not valid:
            return None, error

        # Cria job
        job_id = str(uuid.uuid4())
        job = Job(job_id, input_text, voice_name, image_paths, model_id, skip_formatting)

        logger.info(f"Job criado: {job_id} (skip_formatting={skip_formatting})")

        return job, None

    def process_job(
        self,
        job: Job,
        progress_callback: Optional[Callable[[str, int], None]] = None,
        max_workers_video: int = 3,
        max_batch_retries: int = 3,
        allow_partial_success: bool = True
    ) -> Path:
        """
        Processa um job completo com retry automático para falhas

        Args:
            job: Job a processar
            progress_callback: Função de callback para progresso (message, percent)
            max_workers_video: Número máximo de vídeos processados simultaneamente no WaveSpeed (padrão: 3)
            max_batch_retries: Número máximo de tentativas para batches que falharam
            allow_partial_success: Se True, permite concluir o job mesmo com alguns batches falhados

        Returns:
            Path do vídeo final gerado

        Raises:
            Exception: Se o processamento falhar completamente
        """
        try:
            def update_progress(message: str, percent: int):
                """Helper para atualizar progresso"""
                job.update_progress(message, percent)
                if progress_callback:
                    progress_callback(message, percent)

            logger.info(f"Iniciando processamento do job {job.job_id}")

            # ETAPA 1: Processar texto (com ou sem Gemini)
            if job.skip_formatting:
                update_progress("Dividindo texto em batches...", 5)
            else:
                update_progress("Formatando texto com IA...", 5)
            job.status = JobStatus.PROCESSING_TEXT
            job.save_state()

            job.formatted_texts = self.text_processor.process_text(
                full_text=job.input_text,
                output_dir=job.job_dir,
                progress_callback=lambda msg: update_progress(msg, 10),
                skip_formatting=job.skip_formatting
            )

            total_batches = len(job.formatted_texts)
            if job.skip_formatting:
                update_progress(f"Texto dividido em {total_batches} batches (sem formatação)", 20)
            else:
                update_progress(f"Texto formatado em {total_batches} batches", 20)

            # ETAPA 2: Gerar áudios com ElevenLabs (com retry automático)
            update_progress("Gerando áudios com síntese de voz...", 25)
            job.status = JobStatus.GENERATING_AUDIO
            job.save_state()

            voice_id = self.audio_generator.get_voice_id_by_name(job.voice_name)

            job.audios = self.audio_generator.generate_audios_batch(
                texts=job.formatted_texts,
                voice_id=voice_id,
                output_dir=job.job_dir,
                model_id=job.model_id,
                progress_callback=lambda msg: update_progress(msg, 30),
                max_batch_retries=max_batch_retries
            )

            # Verifica resultados dos áudios
            successful_audios = [a for a in job.audios if not a.get('error')]
            failed_audios = [a for a in job.audios if a.get('error')]

            if failed_audios:
                error_types = {}
                for fa in failed_audios:
                    et = fa.get('error_type', 'UNKNOWN')
                    error_types[et] = error_types.get(et, 0) + 1

                error_summary = ", ".join([f"{et}: {count}" for et, count in error_types.items()])
                logger.warning(f"⚠️ {len(failed_audios)} áudios falharam após retries: {error_summary}")

                if not successful_audios:
                    raise Exception(f"Todos os {len(failed_audios)} áudios falharam ao gerar. Erros: {error_summary}")

                if not allow_partial_success:
                    raise Exception(f"{len(failed_audios)} áudios falharam ao gerar: {error_summary}")

                update_progress(f"⚠️ {len(successful_audios)}/{total_batches} áudios gerados (alguns falharam)", 50)
            else:
                update_progress(f"✅ {len(job.audios)} áudios gerados com sucesso", 50)

            # ETAPA 3: Gerar vídeos com lip-sync (WaveSpeed) - apenas para áudios bem-sucedidos
            audios_para_video = successful_audios
            update_progress(f"Gerando {len(audios_para_video)} vídeos com lip-sync em paralelo...", 55)
            job.status = JobStatus.GENERATING_VIDEO
            job.save_state()

            job.videos = self.video_generator.generate_videos_batch(
                audios=audios_para_video,
                image_paths=job.image_paths,
                output_dir=job.job_dir,
                progress_callback=lambda msg: update_progress(msg, 60),
                max_workers=max_workers_video,
                max_batch_retries=max_batch_retries
            )

            # Verifica resultados dos vídeos
            successful_videos = [v for v in job.videos if not v.get('error')]
            failed_videos = [v for v in job.videos if v.get('error')]

            if failed_videos:
                error_types = {}
                for fv in failed_videos:
                    et = fv.get('error_type', 'UNKNOWN')
                    error_types[et] = error_types.get(et, 0) + 1

                error_summary = ", ".join([f"{et}: {count}" for et, count in error_types.items()])
                logger.warning(f"⚠️ {len(failed_videos)} vídeos falharam após retries: {error_summary}")

                if not successful_videos:
                    raise Exception(f"Todos os {len(failed_videos)} vídeos falharam ao gerar. Erros: {error_summary}")

                if not allow_partial_success:
                    raise Exception(f"{len(failed_videos)} vídeos falharam ao gerar: {error_summary}")

                update_progress(f"⚠️ {len(successful_videos)}/{len(audios_para_video)} vídeos gerados (alguns falharam)", 85)
            else:
                update_progress(f"✅ {len(job.videos)} vídeos gerados com sucesso", 85)

            # ETAPA 4: Concatenar vídeos (mantendo ordem original)
            update_progress("Concatenando vídeos finais...", 90)
            job.status = JobStatus.CONCATENATING
            job.save_state()

            # Ordena vídeos pelo número para manter ordem original do texto
            video_paths = [v['video_path'] for v in sorted(successful_videos, key=lambda x: x['video_number']) if v.get('video_path')]

            if not video_paths:
                raise Exception("Nenhum vídeo disponível para concatenação")

            final_video_path = job.job_dir / 'final_output.mp4'

            final_video_path = self.video_concatenator.concatenate_videos(
                video_paths=video_paths,
                output_path=final_video_path,
                add_transitions=False,  # Pode ativar se desejar transições
                progress_callback=lambda msg: update_progress(msg, 95)
            )

            # Adiciona informações de batches falhados ao job
            total_failed = len(failed_audios) + len(failed_videos)
            total_successful = len(successful_videos)

            if total_failed > 0:
                job.error = f"Concluído com {total_failed} batches falhados (de {total_batches} total)"
                logger.warning(f"Job {job.job_id}: {job.error}")

            # Marca job como concluído
            job.mark_completed(final_video_path)

            # Log resumo
            logger.info(f"🎉 Job {job.job_id} processado!")
            logger.info(f"   - Batches totais: {total_batches}")
            logger.info(f"   - Áudios gerados: {len(successful_audios)}")
            logger.info(f"   - Vídeos gerados: {len(successful_videos)}")
            if failed_audios:
                logger.info(f"   - Áudios falhados: {len(failed_audios)}")
            if failed_videos:
                logger.info(f"   - Vídeos falhados: {len(failed_videos)}")
            logger.info(f"   - Vídeo final: {final_video_path}")

            return final_video_path

        except Exception as e:
            error_msg = f"Erro no processamento: {str(e)}"
            job.mark_failed(error_msg)
            logger.error(f"Job {job.job_id} falhou: {error_msg}")
            raise

    def get_job_estimate(self, input_text: str) -> Dict:
        """
        Estima custo e tempo para processar um texto

        Args:
            input_text: Texto de entrada

        Returns:
            Dict com estimativas:
            {
                'num_batches': 5,
                'num_videos': 5,
                'estimated_time': '10m 30s',
                'estimated_cost': {'total': '$2.50', 'gemini': '$0.10', ...}
            }
        """
        from utils import split_into_paragraphs, create_batches

        paragraphs = split_into_paragraphs(input_text)
        batches = create_batches(paragraphs, Config.BATCH_SIZE)

        num_batches = len(batches)
        num_videos = num_batches
        num_chars = len(input_text)

        estimated_time = estimate_time(num_batches, num_videos)
        estimated_cost = estimate_cost(num_chars, num_videos)

        return {
            'num_batches': num_batches,
            'num_videos': num_videos,
            'num_chars': num_chars,
            'estimated_time': estimated_time,
            'estimated_cost': estimated_cost
        }

def test_job_manager():
    """Função de teste do gerenciador de jobs"""
    print(f"\n{'='*60}")
    print(f"TESTE DO JOB MANAGER")
    print(f"{'='*60}\n")

    manager = JobManager()

    test_text = """
    Olá! Bem-vindo ao nosso canal.

    Hoje vamos falar sobre inteligência artificial.
    É um tema fascinante que está mudando o mundo.

    Fique até o final para aprender mais!
    """

    # Estima job
    estimate = manager.get_job_estimate(test_text)

    print("Estimativa:")
    print(f"  - Batches: {estimate['num_batches']}")
    print(f"  - Vídeos: {estimate['num_videos']}")
    print(f"  - Caracteres: {estimate['num_chars']}")
    print(f"  - Tempo estimado: {estimate['estimated_time']}")
    print(f"  - Custo estimado: {estimate['estimated_cost']['total']}")
    print()

    print("Para testar o processamento completo, use a interface Gradio (app.py)")

if __name__ == "__main__":
    test_job_manager()
