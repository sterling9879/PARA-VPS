"""
Funções auxiliares e utilitárias
"""
import time
import logging
import random
from pathlib import Path
from functools import wraps
from typing import List, Callable, Any
import requests

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_logger(name: str) -> logging.Logger:
    """Retorna um logger configurado"""
    return logging.getLogger(name)

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    exponential: bool = True,
    exceptions: tuple = (requests.HTTPError, requests.RequestException)
):
    """
    Decorador para retry com backoff exponencial

    Args:
        max_retries: Número máximo de tentativas
        base_delay: Delay base em segundos
        exponential: Se True, usa backoff exponencial (2^n)
        exceptions: Tupla de exceções que devem acionar retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = get_logger(func.__name__)

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Falhou após {max_retries} tentativas: {e}")
                        raise

                    # Calcula delay
                    if exponential:
                        delay = base_delay * (2 ** attempt)
                    else:
                        delay = base_delay

                    logger.warning(
                        f"Tentativa {attempt + 1}/{max_retries} falhou: {e}. "
                        f"Aguardando {delay}s antes de tentar novamente..."
                    )
                    time.sleep(delay)

            raise Exception(f"Falhou após {max_retries} tentativas")

        return wrapper
    return decorator

def validate_images(image_paths: List[str]) -> tuple[bool, str]:
    """
    Valida lista de imagens

    Returns:
        (válido, mensagem_erro)
    """
    from config import Config

    if not image_paths:
        return False, "Nenhuma imagem fornecida"

    if len(image_paths) < Config.MIN_IMAGES:
        return False, f"Mínimo de {Config.MIN_IMAGES} imagem(ns) necessária(s)"

    if len(image_paths) > Config.MAX_IMAGES:
        return False, f"Máximo de {Config.MAX_IMAGES} imagens permitidas"

    for img_path in image_paths:
        path = Path(img_path)

        if not path.exists():
            return False, f"Imagem não encontrada: {img_path}"

        if path.suffix.lower() not in Config.SUPPORTED_IMAGE_FORMATS:
            return False, f"Formato não suportado: {path.suffix}. Use PNG, JPG ou JPEG"

        # Verifica se não está corrompida
        try:
            from PIL import Image
            img = Image.open(path)
            img.verify()
        except Exception as e:
            return False, f"Imagem corrompida: {img_path} - {e}"

    return True, "OK"

def validate_text(text: str) -> tuple[bool, str]:
    """
    Valida texto de entrada

    Returns:
        (válido, mensagem_erro)
    """
    from config import Config

    if not text or not text.strip():
        return False, "Texto vazio"

    text_length = len(text.strip())

    if text_length < Config.MIN_TEXT_LENGTH:
        return False, f"Texto muito curto. Mínimo: {Config.MIN_TEXT_LENGTH} caracteres"

    if text_length > Config.MAX_TEXT_LENGTH:
        return False, f"Texto muito longo. Máximo: {Config.MAX_TEXT_LENGTH} caracteres"

    return True, "OK"

def split_into_paragraphs(text: str) -> List[str]:
    """
    Divide texto em parágrafos

    Args:
        text: Texto completo

    Returns:
        Lista de parágrafos não vazios
    """
    # Remove espaços extras e divide por quebras de linha
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    return paragraphs

def create_batches(items: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Divide lista em batches

    Args:
        items: Lista de itens
        batch_size: Tamanho de cada batch

    Returns:
        Lista de batches
    """
    batches = []
    for i in range(0, len(items), batch_size):
        batches.append(items[i:i + batch_size])
    return batches

def select_random_image(image_pool: List[Path], used_images: List[Path] = None) -> Path:
    """
    Seleciona uma imagem aleatória do pool, evitando repetições consecutivas

    Args:
        image_pool: Pool de imagens disponíveis
        used_images: Lista de imagens usadas recentemente

    Returns:
        Path da imagem selecionada
    """
    if not used_images or len(image_pool) == 1:
        return random.choice(image_pool)

    # Tenta evitar a última imagem usada
    last_used = used_images[-1] if used_images else None
    available = [img for img in image_pool if img != last_used]

    if available:
        return random.choice(available)
    else:
        return random.choice(image_pool)

def format_time(seconds: float) -> str:
    """
    Formata tempo em segundos para string legível

    Args:
        seconds: Tempo em segundos

    Returns:
        String formatada (ex: "2m 30s")
    """
    if seconds < 60:
        return f"{int(seconds)}s"

    minutes = int(seconds // 60)
    secs = int(seconds % 60)

    if minutes < 60:
        return f"{minutes}m {secs}s"

    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m {secs}s"

def estimate_cost(num_chars: int, num_videos: int) -> dict:
    """
    Estima custo do processamento

    Args:
        num_chars: Número total de caracteres
        num_videos: Número de vídeos a gerar

    Returns:
        Dict com estimativas de custo
    """
    # Custos aproximados (em USD)
    GEMINI_COST_PER_1M_CHARS = 0.10
    ELEVENLABS_COST_PER_1K_CHARS = 0.30
    WAVESPEED_COST_PER_VIDEO = 0.20

    gemini_cost = (num_chars / 1_000_000) * GEMINI_COST_PER_1M_CHARS
    elevenlabs_cost = (num_chars / 1_000) * ELEVENLABS_COST_PER_1K_CHARS
    wavespeed_cost = num_videos * WAVESPEED_COST_PER_VIDEO

    total_cost = gemini_cost + elevenlabs_cost + wavespeed_cost

    return {
        'gemini': f"${gemini_cost:.2f}",
        'elevenlabs': f"${elevenlabs_cost:.2f}",
        'wavespeed': f"${wavespeed_cost:.2f}",
        'total': f"${total_cost:.2f}"
    }

def estimate_time(num_batches: int, num_videos: int) -> str:
    """
    Estima tempo total de processamento

    Args:
        num_batches: Número de batches de texto
        num_videos: Número de vídeos

    Returns:
        String com estimativa de tempo
    """
    # Tempos médios (em segundos)
    GEMINI_TIME_PER_BATCH = 3
    ELEVENLABS_TIME_PER_AUDIO = 5
    WAVESPEED_TIME_PER_VIDEO = 120
    FFMPEG_TIME = 10

    total_seconds = (
        num_batches * GEMINI_TIME_PER_BATCH +
        num_videos * ELEVENLABS_TIME_PER_AUDIO +
        num_videos * WAVESPEED_TIME_PER_VIDEO +
        FFMPEG_TIME
    )

    return format_time(total_seconds)
