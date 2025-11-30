"""
Módulo de geração de áudio usando ElevenLabs ou MiniMax API
"""
from elevenlabs import ElevenLabs
import requests
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import Config
from utils import get_logger, retry_with_backoff

logger = get_logger(__name__)


class MiniMaxClient:
    """Cliente para MiniMax Audio API"""

    def __init__(self, api_key: str):
        """
        Inicializa o cliente MiniMax

        Args:
            api_key: Chave da API MiniMax
        """
        self.api_key = api_key
        self.base_url = "https://api.minimax.chat/v1/text_to_speech"
        self.session = requests.Session()
        logger.info("MiniMaxClient inicializado")

    def get_available_voices(self) -> List[Dict[str, str]]:
        """
        Retorna lista de vozes disponíveis do MiniMax

        Returns:
            Lista de dicts com informações das vozes
        """
        # Vozes pré-definidas do MiniMax (baseado na documentação)
        # Você pode expandir esta lista conforme a documentação oficial
        return [
            {'voice_id': 'male-qn-qingse', 'name': 'Male Qingse (CN)', 'language': 'zh'},
            {'voice_id': 'male-qn-jingying', 'name': 'Male Jingying (CN)', 'language': 'zh'},
            {'voice_id': 'male-qn-badao', 'name': 'Male Badao (CN)', 'language': 'zh'},
            {'voice_id': 'female-shaonv', 'name': 'Female Shaonv (CN)', 'language': 'zh'},
            {'voice_id': 'female-yujie', 'name': 'Female Yujie (CN)', 'language': 'zh'},
            {'voice_id': 'female-chengshu', 'name': 'Female Chengshu (CN)', 'language': 'zh'},
            {'voice_id': 'presenter_male', 'name': 'Presenter Male', 'language': 'en'},
            {'voice_id': 'presenter_female', 'name': 'Presenter Female', 'language': 'en'},
        ]

    @retry_with_backoff(max_retries=3, base_delay=2.0)
    def generate_audio(
        self,
        text: str,
        voice_id: str = "female-shaonv",
        output_path: Path = None,
        speed: float = 1.0,
        vol: float = 1.0,
        pitch: int = 0,
        output_format: str = "mp3"
    ) -> Path:
        """
        Gera áudio a partir de texto usando MiniMax

        Args:
            text: Texto para sintetizar
            voice_id: ID da voz a usar
            output_path: Caminho para salvar o áudio
            speed: Velocidade da fala (0.5 a 2.0)
            vol: Volume (0.1 a 10.0)
            pitch: Ajuste de tom (-12 a 12)
            output_format: Formato de saída (mp3, wav, flac, pcm)

        Returns:
            Path do arquivo de áudio gerado

        Raises:
            Exception: Se a geração falhar
        """
        try:
            logger.info(f"Gerando áudio MiniMax para: {output_path.name if output_path else 'temp'}")

            payload = {
                "text": text,
                "voice_setting": {
                    "voice_id": voice_id,
                    "speed": speed,
                    "vol": vol,
                    "pitch": pitch
                },
                "audio_setting": {
                    "format": output_format,
                    "sample_rate": 32000,
                    "bitrate": 128000,
                    "channel": 1
                }
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            response = self.session.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            response.raise_for_status()
            data = response.json()

            # Verifica se há erro
            if data.get("base_resp", {}).get("status_code") != 0:
                error_msg = data.get("base_resp", {}).get("status_msg", "Erro desconhecido")
                raise Exception(f"MiniMax API error: {error_msg}")

            # Obtém o áudio (pode ser hex ou URL dependendo da implementação)
            audio_data = data.get("data", {}).get("audio")

            if not audio_data:
                raise Exception("Nenhum dado de áudio retornado pela API MiniMax")

            # Salva arquivo
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Se for hex string, decodifica
            if isinstance(audio_data, str) and all(c in '0123456789abcdefABCDEF' for c in audio_data[:100]):
                audio_bytes = bytes.fromhex(audio_data)
                with open(output_path, 'wb') as f:
                    f.write(audio_bytes)
            # Se for URL, baixa o arquivo
            elif isinstance(audio_data, str) and audio_data.startswith('http'):
                audio_response = requests.get(audio_data, timeout=120)
                audio_response.raise_for_status()
                with open(output_path, 'wb') as f:
                    f.write(audio_response.content)
            else:
                raise Exception(f"Formato de áudio desconhecido: {type(audio_data)}")

            logger.info(f"Áudio MiniMax gerado com sucesso: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Erro ao gerar áudio MiniMax: {e}")
            raise

class AudioGenerator:
    """Gera áudios usando ElevenLabs ou MiniMax API"""

    def __init__(self, provider: str = None):
        """
        Inicializa o gerador de áudio

        Args:
            provider: 'elevenlabs' ou 'minimax' (padrão: config ou elevenlabs)
        """
        if provider is None:
            provider = Config.AUDIO_PROVIDER

        self.provider = provider.lower()
        self.available_voices = None

        # Inicializa o cliente apropriado
        if self.provider == 'elevenlabs':
            if not Config.ELEVENLABS_API_KEY:
                raise ValueError("ELEVENLABS_API_KEY não configurada")
            self.client = ElevenLabs(api_key=Config.ELEVENLABS_API_KEY)
            logger.info("AudioGenerator inicializado com ElevenLabs")

        elif self.provider == 'minimax':
            if not Config.MINIMAX_API_KEY:
                raise ValueError("MINIMAX_API_KEY não configurada")
            self.client = MiniMaxClient(api_key=Config.MINIMAX_API_KEY)
            logger.info("AudioGenerator inicializado com MiniMax")

        else:
            raise ValueError(f"Provedor de áudio inválido: {provider}. Use 'elevenlabs' ou 'minimax'")

    def get_available_voices(self) -> List[Dict[str, str]]:
        """
        Obtém lista de vozes disponíveis (ElevenLabs ou MiniMax)

        Returns:
            Lista de dicts com informações das vozes:
            [
                {'voice_id': 'xxx', 'name': 'Rachel', 'labels': {...}},
                ...
            ]
        """
        try:
            if self.available_voices is None:
                logger.info(f"Buscando vozes disponíveis do {self.provider}...")

                if self.provider == 'elevenlabs':
                    voices = self.client.voices.get_all()
                    self.available_voices = [
                        {
                            'voice_id': voice.voice_id,
                            'name': voice.name,
                            'labels': voice.labels if hasattr(voice, 'labels') else {}
                        }
                        for voice in voices.voices
                    ]

                elif self.provider == 'minimax':
                    self.available_voices = self.client.get_available_voices()

                logger.info(f"Encontradas {len(self.available_voices)} vozes disponíveis")

            return self.available_voices

        except Exception as e:
            logger.error(f"Erro ao buscar vozes do {self.provider}: {e}")
            # Retorna vozes padrão em caso de erro
            return [
                {'voice_id': 'default', 'name': 'Default Voice', 'labels': {}}
            ]

    def get_voice_id_by_name(self, voice_name: str) -> str:
        """
        Obtém voice_id pelo nome da voz

        Args:
            voice_name: Nome da voz

        Returns:
            voice_id correspondente ou primeiro voice_id disponível
        """
        voices = self.get_available_voices()

        for voice in voices:
            if voice['name'].lower() == voice_name.lower():
                return voice['voice_id']

        # Se não encontrar, retorna a primeira voz disponível
        if voices:
            logger.warning(f"Voz '{voice_name}' não encontrada. Usando '{voices[0]['name']}'")
            return voices[0]['voice_id']

        logger.error("Nenhuma voz disponível")
        return 'default'

    @retry_with_backoff(max_retries=3, base_delay=2.0)
    def generate_audio(
        self,
        text: str,
        voice_id: str,
        output_path: Path,
        model_id: str = "eleven_multilingual_v2"
    ) -> Path:
        """
        Gera áudio a partir de texto (ElevenLabs ou MiniMax)

        Args:
            text: Texto para sintetizar
            voice_id: ID da voz a usar
            output_path: Caminho para salvar o áudio
            model_id: Modelo a usar (relevante apenas para ElevenLabs)

        Returns:
            Path do arquivo de áudio gerado

        Raises:
            Exception: Se a geração falhar após retries
        """
        try:
            logger.info(f"Gerando áudio ({self.provider}) para: {output_path.name}")

            if self.provider == 'elevenlabs':
                # Gera áudio usando ElevenLabs (sintaxe v3)
                audio_data = self.client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_id,
                    model_id=model_id,
                    output_format="mp3_44100_128"
                )

                # Salva arquivo
                output_path.parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, 'wb') as f:
                    # audio_data é um iterador de bytes
                    for chunk in audio_data:
                        f.write(chunk)

            elif self.provider == 'minimax':
                # Gera áudio usando MiniMax
                return self.client.generate_audio(
                    text=text,
                    voice_id=voice_id,
                    output_path=output_path,
                    speed=1.0,
                    vol=1.0,
                    pitch=0,
                    output_format="mp3"
                )

            logger.info(f"Áudio gerado com sucesso: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Erro ao gerar áudio para {output_path.name}: {e}")
            raise

    def generate_audios_batch(
        self,
        texts: List[Dict],
        voice_id: str,
        output_dir: Path,
        model_id: str = "eleven_multilingual_v2",
        progress_callback=None,
        max_workers: int = None
    ) -> List[Dict]:
        """
        Gera múltiplos áudios em paralelo

        Args:
            texts: Lista de dicts com textos formatados
                   [{'batch_number': 1, 'formatted_text': '...', ...}, ...]
            voice_id: ID da voz a usar
            output_dir: Diretório para salvar áudios
            model_id: Modelo ElevenLabs a usar (padrão: eleven_v3)
            progress_callback: Função de callback para progresso
            max_workers: Número máximo de workers paralelos (None = auto)

        Returns:
            Lista de dicts com informações dos áudios gerados
            [
                {
                    'audio_number': 1,
                    'text': '...',
                    'audio_path': Path('audio_1.mp3'),
                    'duration': 45.2  # em segundos (se disponível)
                },
                ...
            ]
        """
        import time

        logger.info(f"Iniciando geração de {len(texts)} áudios")

        # Cria diretório de áudios
        audio_dir = output_dir / 'audios'
        audio_dir.mkdir(parents=True, exist_ok=True)

        # Determina número de workers baseado no provider
        if max_workers is None:
            if self.provider == 'elevenlabs':
                # ElevenLabs tem limite de 5 requisições simultâneas, usamos 3 para segurança
                max_workers = min(Config.ELEVENLABS_MAX_CONCURRENT, len(texts))
            else:
                max_workers = min(Config.MAX_CONCURRENT_REQUESTS, len(texts))

        logger.info(f"Usando {max_workers} workers paralelos para {self.provider}")

        results = []

        def generate_single_audio_with_retry(text_data: Dict, max_retries: int = 3) -> Dict:
            """Gera um único áudio com retry para erros 429"""
            audio_number = text_data['batch_number']
            text = text_data['formatted_text']
            audio_path = audio_dir / f'audio_{audio_number}.mp3'

            if progress_callback:
                progress_callback(f"Gerando áudio {audio_number}/{len(texts)}...")

            last_error = None
            for attempt in range(max_retries):
                try:
                    generated_path = self.generate_audio(
                        text=text,
                        voice_id=voice_id,
                        output_path=audio_path,
                        model_id=model_id
                    )

                    return {
                        'audio_number': audio_number,
                        'text': text,
                        'audio_path': generated_path,
                        'duration': None
                    }

                except Exception as e:
                    last_error = e
                    error_str = str(e).lower()

                    # Se for erro 429 (rate limit), espera e tenta novamente
                    if '429' in error_str or 'too_many' in error_str or 'rate' in error_str:
                        wait_time = (attempt + 1) * 5  # 5s, 10s, 15s
                        logger.warning(f"Rate limit atingido para áudio {audio_number}. Aguardando {wait_time}s antes de retry {attempt + 1}/{max_retries}")
                        time.sleep(wait_time)
                    else:
                        # Para outros erros, não faz retry
                        break

            # Se chegou aqui, todas as tentativas falharam
            raise last_error

        # Processa em paralelo com controle de concorrência
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(generate_single_audio_with_retry, text_data): text_data
                for text_data in texts
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"Áudio {result['audio_number']} concluído")
                except Exception as e:
                    text_data = futures[future]
                    logger.error(f"Erro ao gerar áudio {text_data['batch_number']}: {e}")
                    # Continua mesmo se um áudio falhar
                    results.append({
                        'audio_number': text_data['batch_number'],
                        'text': text_data['formatted_text'],
                        'audio_path': None,
                        'error': str(e)
                    })

        # Ordena resultados por número
        results.sort(key=lambda x: x['audio_number'])

        logger.info(f"Geração de áudios concluída: {len(results)} áudios")

        return results

def test_audio_generator():
    """Função de teste do gerador de áudio"""
    from pathlib import Path
    import tempfile

    generator = AudioGenerator()

    print(f"\n{'='*60}")
    print(f"TESTE DO AUDIO GENERATOR")
    print(f"{'='*60}\n")

    # Lista vozes disponíveis
    print("Vozes disponíveis:")
    voices = generator.get_available_voices()
    for voice in voices[:5]:  # Mostra apenas as 5 primeiras
        print(f"  - {voice['name']} (ID: {voice['voice_id']})")
    print()

    # Testa geração de áudio
    test_texts = [
        {
            'batch_number': 1,
            'formatted_text': 'Olá! Este é um teste de geração de áudio.'
        },
        {
            'batch_number': 2,
            'formatted_text': 'A inteligência artificial está transformando o mundo.'
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        voice_id = generator.get_voice_id_by_name(voices[0]['name'])

        results = generator.generate_audios_batch(
            texts=test_texts,
            voice_id=voice_id,
            output_dir=Path(tmpdir)
        )

        print("Áudios gerados:")
        for result in results:
            if result.get('audio_path'):
                print(f"  - Áudio {result['audio_number']}: {result['audio_path']}")
            else:
                print(f"  - Áudio {result['audio_number']}: ERRO - {result.get('error')}")

if __name__ == "__main__":
    test_audio_generator()
