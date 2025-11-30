"""
Módulo de processamento e formatação de texto usando Gemini 2.5 Flash
"""
import google.generativeai as genai
from pathlib import Path
from typing import List, Dict
from config import Config
from utils import get_logger, retry_with_backoff, create_batches, split_into_paragraphs

logger = get_logger(__name__)

class TextProcessor:
    """Processa e formata texto usando Gemini API"""

    def __init__(self):
        """Inicializa o processador de texto"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
        logger.info("TextProcessor inicializado com Gemini 2.5 Flash Lite")

    def _get_formatting_prompt(self, batch_text: str, batch_number: int) -> str:
        """
        Retorna o prompt de formatação para o Gemini

        IMPORTANTE: Este é um prompt MODELO que deve ser customizado
        pelo usuário conforme suas necessidades específicas.

        Args:
            batch_text: Texto do batch a ser formatado
            batch_number: Número do batch (para contexto)

        Returns:
            Prompt formatado
        """
        return f"""Você é um especialista em roteirização e formatação de texto para narração em vídeo.

Sua tarefa é otimizar o seguinte texto para ser narrado em um vídeo com sincronização labial (lip-sync).

BATCH #{batch_number}:
{batch_text}

INSTRUÇÕES DE FORMATAÇÃO:
1. Mantenha o conteúdo original, mas melhore a fluidez e naturalidade da narração
2. Ajuste frases longas para facilitar a respiração natural do narrador
3. Remova vícios de linguagem e repetições desnecessárias
4. Adicione pausas naturais onde apropriado (use "..." para pausas curtas)
5. Mantenha o tom e estilo apropriado para vídeo profissional
6. Garanta que o texto seja claro e fácil de entender quando falado
7. Preserve informações importantes e a mensagem principal
8. O texto deve soar natural quando lido em voz alta

FORMATO DE SAÍDA:
Retorne APENAS o texto formatado, sem comentários adicionais ou explicações.
Mantenha a estrutura de parágrafos original quando fizer sentido.

TEXTO FORMATADO:"""

    @retry_with_backoff(max_retries=3, base_delay=2.0)
    def format_batch(self, batch_text: str, batch_number: int) -> str:
        """
        Formata um batch de texto usando Gemini

        Args:
            batch_text: Texto do batch
            batch_number: Número do batch

        Returns:
            Texto formatado

        Raises:
            Exception: Se a formatação falhar após retries
        """
        try:
            logger.info(f"Formatando batch #{batch_number}...")

            prompt = self._get_formatting_prompt(batch_text, batch_number)

            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'top_k': 40,
                    'max_output_tokens': 8192,
                }
            )

            formatted_text = response.text.strip()

            logger.info(f"Batch #{batch_number} formatado com sucesso ({len(formatted_text)} caracteres)")

            return formatted_text

        except Exception as e:
            logger.error(f"Erro ao formatar batch #{batch_number}: {e}")
            raise

    def process_text(
        self,
        full_text: str,
        output_dir: Path,
        progress_callback=None
    ) -> List[Dict[str, any]]:
        """
        Processa texto completo em batches

        Args:
            full_text: Texto completo a processar
            output_dir: Diretório para salvar textos formatados
            progress_callback: Função de callback para progresso (opcional)

        Returns:
            Lista de dicts com informações dos batches processados
            [
                {
                    'batch_number': 1,
                    'original_text': '...',
                    'formatted_text': '...',
                    'file_path': Path('batch_1.txt')
                },
                ...
            ]
        """
        logger.info("Iniciando processamento de texto")

        # Divide em parágrafos
        paragraphs = split_into_paragraphs(full_text)
        logger.info(f"Texto dividido em {len(paragraphs)} parágrafos")

        # Cria batches
        batches = create_batches(paragraphs, Config.BATCH_SIZE)
        logger.info(f"Criados {len(batches)} batches de {Config.BATCH_SIZE} parágrafos cada")

        # Cria diretório de saída
        formatted_dir = output_dir / 'formatted_text'
        formatted_dir.mkdir(parents=True, exist_ok=True)

        results = []

        for idx, batch in enumerate(batches, start=1):
            batch_number = idx

            # Junta parágrafos do batch
            batch_text = '\n\n'.join(batch)

            # Atualiza progresso
            if progress_callback:
                progress_callback(f"Formatando texto batch {batch_number}/{len(batches)}...")

            # Formata batch
            formatted_text = self.format_batch(batch_text, batch_number)

            # Salva em arquivo
            file_path = formatted_dir / f'batch_{batch_number}.txt'
            file_path.write_text(formatted_text, encoding='utf-8')

            logger.info(f"Batch {batch_number} salvo em: {file_path}")

            results.append({
                'batch_number': batch_number,
                'original_text': batch_text,
                'formatted_text': formatted_text,
                'file_path': file_path
            })

        logger.info(f"Processamento de texto concluído: {len(results)} batches")

        return results

def test_text_processor():
    """Função de teste do processador de texto"""
    from pathlib import Path
    import tempfile

    # Texto de exemplo
    test_text = """
    Olá! Bem-vindo ao nosso vídeo sobre inteligência artificial.

    A inteligência artificial está transformando o mundo como conhecemos.
    Ela está presente em nosso dia a dia de formas que muitas vezes não percebemos.

    Neste vídeo, vamos explorar como a IA funciona e seu impacto na sociedade.
    Você vai aprender sobre machine learning, deep learning e muito mais.

    Fique conosco e descubra o fascinante mundo da inteligência artificial!
    Não se esqueça de se inscrever no canal e ativar as notificações.
    """

    # Cria processador
    processor = TextProcessor()

    # Processa texto
    with tempfile.TemporaryDirectory() as tmpdir:
        results = processor.process_text(test_text, Path(tmpdir))

        print(f"\n{'='*60}")
        print(f"TESTE DO TEXT PROCESSOR")
        print(f"{'='*60}\n")

        for result in results:
            print(f"Batch #{result['batch_number']}:")
            print(f"Original ({len(result['original_text'])} chars):")
            print(result['original_text'])
            print(f"\nFormatado ({len(result['formatted_text'])} chars):")
            print(result['formatted_text'])
            print(f"\nSalvo em: {result['file_path']}")
            print(f"\n{'-'*60}\n")

if __name__ == "__main__":
    test_text_processor()
