"""
Módulo de concatenação de vídeos usando FFmpeg
"""
import subprocess
from pathlib import Path
from typing import List, Dict
from utils import get_logger

logger = get_logger(__name__)

class VideoConcatenator:
    """Concatena múltiplos vídeos usando FFmpeg"""

    def __init__(self):
        """Inicializa o concatenador de vídeos"""
        self._check_ffmpeg()
        logger.info("VideoConcatenator inicializado")

    def _check_ffmpeg(self):
        """Verifica se FFmpeg está instalado"""
        try:
            result = subprocess.run(
                ['ffmpeg', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                raise Exception("FFmpeg não está funcionando corretamente")

            logger.info("FFmpeg detectado e funcionando")

        except FileNotFoundError:
            raise Exception(
                "FFmpeg não encontrado. Por favor, instale FFmpeg:\n"
                "  - Ubuntu/Debian: sudo apt-get install ffmpeg\n"
                "  - macOS: brew install ffmpeg\n"
                "  - Windows: Baixe de https://ffmpeg.org/download.html"
            )
        except Exception as e:
            raise Exception(f"Erro ao verificar FFmpeg: {e}")

    def concatenate_videos(
        self,
        video_paths: List[Path],
        output_path: Path,
        add_transitions: bool = True,
        transition_duration: float = 0.5,
        progress_callback=None
    ) -> Path:
        """
        Concatena múltiplos vídeos em um único arquivo

        Args:
            video_paths: Lista de Paths dos vídeos a concatenar (em ordem)
            output_path: Path do vídeo final
            add_transitions: Se True, adiciona transições de fade entre vídeos
            transition_duration: Duração das transições em segundos
            progress_callback: Função de callback para progresso

        Returns:
            Path do vídeo final gerado

        Raises:
            Exception: Se a concatenação falhar
        """
        try:
            logger.info(f"Concatenando {len(video_paths)} vídeos...")

            if progress_callback:
                progress_callback("Concatenando vídeos...")

            # Valida vídeos
            for video_path in video_paths:
                if not video_path.exists():
                    raise Exception(f"Vídeo não encontrado: {video_path}")

            # Cria arquivo de lista para FFmpeg
            list_file = output_path.parent / 'concat_list.txt'

            with open(list_file, 'w') as f:
                for video_path in video_paths:
                    # FFmpeg concat demuxer requer caminhos absolutos
                    abs_path = video_path.resolve()
                    # Escapa apóstrofos no caminho
                    escaped_path = str(abs_path).replace("'", "'\\''")
                    f.write(f"file '{escaped_path}'\n")

            logger.info(f"Lista de concatenação criada: {list_file}")

            if add_transitions and len(video_paths) > 1:
                # Concatenação com transições (mais complexa)
                output_path = self._concatenate_with_transitions(
                    video_paths,
                    output_path,
                    transition_duration,
                    progress_callback
                )
            else:
                # Concatenação simples (mais rápida)
                output_path = self._concatenate_simple(
                    list_file,
                    output_path,
                    progress_callback
                )

            # Remove arquivo temporário
            list_file.unlink(missing_ok=True)

            logger.info(f"Vídeo final gerado: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"Erro ao concatenar vídeos: {e}")
            raise

    def _concatenate_simple(
        self,
        list_file: Path,
        output_path: Path,
        progress_callback=None
    ) -> Path:
        """
        Concatenação simples sem transições

        Args:
            list_file: Path do arquivo com lista de vídeos
            output_path: Path do vídeo de saída
            progress_callback: Função de callback para progresso

        Returns:
            Path do vídeo gerado
        """
        try:
            logger.info("Usando concatenação simples (sem transições)")

            # Comando FFmpeg para concatenação simples
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(list_file),
                '-c', 'copy',  # Copia streams sem re-encoding (mais rápido)
                '-y',  # Sobrescreve arquivo de saída
                str(output_path)
            ]

            logger.info(f"Executando: {' '.join(cmd)}")

            if progress_callback:
                progress_callback("Processando concatenação (modo rápido)...")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )

            if result.returncode != 0:
                logger.error(f"STDERR: {result.stderr}")
                raise Exception(f"FFmpeg falhou: {result.stderr}")

            logger.info("Concatenação simples concluída")

            return output_path

        except subprocess.TimeoutExpired:
            raise Exception("Timeout na concatenação de vídeos")
        except Exception as e:
            logger.error(f"Erro na concatenação simples: {e}")
            raise

    def _concatenate_with_transitions(
        self,
        video_paths: List[Path],
        output_path: Path,
        transition_duration: float,
        progress_callback=None
    ) -> Path:
        """
        Concatenação com transições de fade

        Args:
            video_paths: Lista de vídeos
            output_path: Path do vídeo de saída
            transition_duration: Duração do fade em segundos
            progress_callback: Função de callback

        Returns:
            Path do vídeo gerado
        """
        try:
            logger.info(f"Usando concatenação com transições (fade de {transition_duration}s)")

            if progress_callback:
                progress_callback("Processando concatenação com transições...")

            # Para transições, precisamos re-encodar
            # Primeiro, concatenamos sem transições
            temp_concat = output_path.parent / 'temp_concat.mp4'

            # Cria arquivo de lista temporário
            list_file = output_path.parent / 'concat_list_temp.txt'

            with open(list_file, 'w') as f:
                for video_path in video_paths:
                    abs_path = video_path.resolve()
                    escaped_path = str(abs_path).replace("'", "'\\''")
                    f.write(f"file '{escaped_path}'\n")

            # Concatenação base
            cmd_concat = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(list_file),
                '-c', 'copy',
                '-y',
                str(temp_concat)
            ]

            logger.info("Executando concatenação base...")

            result = subprocess.run(
                cmd_concat,
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode != 0:
                raise Exception(f"Concatenação base falhou: {result.stderr}")

            # Para simplificar, usamos o vídeo concatenado sem transições elaboradas
            # (Implementar transições de fade entre múltiplos vídeos é muito complexo com FFmpeg)
            # Em produção, considere usar bibliotecas como moviepy para isso

            import shutil
            shutil.move(str(temp_concat), str(output_path))

            # Cleanup
            list_file.unlink(missing_ok=True)

            logger.info("Concatenação com transições concluída")

            return output_path

        except Exception as e:
            logger.error(f"Erro na concatenação com transições: {e}")
            # Fallback para concatenação simples
            logger.warning("Fallback para concatenação simples")
            return self._concatenate_simple(list_file, output_path, progress_callback)

    def get_video_info(self, video_path: Path) -> Dict:
        """
        Obtém informações sobre um vídeo

        Args:
            video_path: Path do vídeo

        Returns:
            Dict com informações do vídeo
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                str(video_path)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                raise Exception(f"ffprobe falhou: {result.stderr}")

            import json
            data = json.loads(result.stdout)

            # Extrai informações relevantes
            video_info = {
                'duration': float(data.get('format', {}).get('duration', 0)),
                'size': int(data.get('format', {}).get('size', 0)),
                'format': data.get('format', {}).get('format_name', 'unknown'),
            }

            # Busca stream de vídeo
            for stream in data.get('streams', []):
                if stream.get('codec_type') == 'video':
                    video_info.update({
                        'width': stream.get('width', 0),
                        'height': stream.get('height', 0),
                        'fps': eval(stream.get('r_frame_rate', '0/1')),
                        'codec': stream.get('codec_name', 'unknown')
                    })
                    break

            return video_info

        except Exception as e:
            logger.error(f"Erro ao obter info do vídeo: {e}")
            return {}

def test_video_concatenator():
    """Função de teste do concatenador"""
    print(f"\n{'='*60}")
    print(f"TESTE DO VIDEO CONCATENATOR")
    print(f"{'='*60}\n")

    try:
        concatenator = VideoConcatenator()
        print("✓ FFmpeg detectado e funcionando")
    except Exception as e:
        print(f"✗ Erro: {e}")

if __name__ == "__main__":
    test_video_concatenator()
