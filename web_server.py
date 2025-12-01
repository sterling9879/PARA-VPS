"""
Servidor Web Flask para Geração de Vídeos com Lip-Sync
Interface web moderna com configuração de API keys integrada
Sistema de autenticação integrado
"""
import os
import json
import secrets
from pathlib import Path
from functools import wraps
from typing import List, Dict, Any, Optional
from flask import Flask, request, jsonify, send_from_directory, send_file, session, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import logging

from config import Config
from job_manager import JobManager
from audio_generator import AudioGenerator  
from utils import get_logger, split_into_paragraphs, create_batches
from database import db

# Configuração de logging
logger = get_logger(__name__)

# Inicialização do Flask
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app, supports_credentials=True)

# Configurações
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

UPLOAD_FOLDER = Path('./temp/uploads')
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

# Credenciais de autenticação (do .env)
AUTH_EMAIL = os.getenv('AUTH_EMAIL', 'admin')
AUTH_PASSWORD = os.getenv('AUTH_PASSWORD', 'Senha#1234')

# ============================================================================
# AUTENTICAÇÃO
# ============================================================================

def login_required(f):
    """Decorador para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            # Se for requisição AJAX/API, retorna 401
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'error': 'Não autenticado', 'redirect': '/login'}), 401
            # Se for requisição normal, redireciona para login
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login')
def login_page():
    """Página de login"""
    if session.get('logged_in'):
        return redirect('/')
    return send_from_directory('static', 'login.html')

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """API de login"""
    try:
        data = request.json
        email = data.get('email', '').strip()
        password = data.get('password', '')

        # Verifica credenciais
        if email == AUTH_EMAIL and password == AUTH_PASSWORD:
            session['logged_in'] = True
            session['user'] = email
            session.permanent = True
            logger.info(f"Login bem-sucedido: {email}")
            return jsonify({'success': True, 'message': 'Login realizado com sucesso'})
        else:
            logger.warning(f"Tentativa de login falhou: {email}")
            return jsonify({'success': False, 'error': 'Email ou senha incorretos'}), 401

    except Exception as e:
        logger.error(f"Erro no login: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    """API de logout"""
    session.clear()
    return jsonify({'success': True, 'message': 'Logout realizado com sucesso'})

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Verifica status de autenticação"""
    return jsonify({
        'success': True,
        'logged_in': session.get('logged_in', False),
        'user': session.get('user', None)
    })

# ============================================================================
# API - LOGS EM TEMPO REAL
# ============================================================================

import subprocess
import threading
import queue
import time

# Fila global para armazenar logs
log_queue = queue.Queue(maxsize=1000)
log_history = []

def read_system_logs():
    """Lê logs do sistema em background"""
    global log_history
    try:
        # Lê logs do journalctl para o serviço lipsync
        process = subprocess.Popen(
            ['journalctl', '-u', 'lipsync', '-f', '-n', '0', '--no-pager'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in iter(process.stdout.readline, ''):
            if line:
                log_entry = {
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'message': line.strip(),
                    'type': 'info'
                }

                # Detecta tipo de log
                if 'ERROR' in line.upper() or 'error' in line.lower():
                    log_entry['type'] = 'error'
                elif 'WARNING' in line.upper() or 'warn' in line.lower():
                    log_entry['type'] = 'warning'
                elif 'SUCCESS' in line.upper() or 'sucesso' in line.lower():
                    log_entry['type'] = 'success'

                # Adiciona ao histórico (máximo 500 linhas)
                log_history.append(log_entry)
                if len(log_history) > 500:
                    log_history = log_history[-500:]

    except Exception as e:
        logger.error(f"Erro ao ler logs do sistema: {e}")

# Inicia thread de leitura de logs (apenas em produção)
if not app.debug:
    log_thread = threading.Thread(target=read_system_logs, daemon=True)
    log_thread.start()

@app.route('/api/logs', methods=['GET'])
@login_required
def get_logs():
    """Retorna logs do sistema"""
    try:
        # Parâmetros
        limit = int(request.args.get('limit', 100))
        log_type = request.args.get('type', None)  # info, warning, error, success

        logs = log_history[-limit:]

        # Filtra por tipo se especificado
        if log_type:
            logs = [l for l in logs if l['type'] == log_type]

        return jsonify({
            'success': True,
            'logs': logs,
            'total': len(log_history)
        })

    except Exception as e:
        logger.error(f"Erro ao obter logs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logs/system', methods=['GET'])
@login_required
def get_system_logs():
    """Retorna últimas linhas do log do sistema via journalctl"""
    try:
        lines = int(request.args.get('lines', 50))

        # Executa journalctl para pegar logs recentes
        result = subprocess.run(
            ['journalctl', '-u', 'lipsync', '-n', str(lines), '--no-pager'],
            capture_output=True,
            text=True,
            timeout=10
        )

        log_lines = []
        for line in result.stdout.strip().split('\n'):
            if line:
                log_entry = {
                    'message': line,
                    'type': 'info'
                }

                if 'ERROR' in line.upper() or 'error' in line.lower():
                    log_entry['type'] = 'error'
                elif 'WARNING' in line.upper() or 'warn' in line.lower():
                    log_entry['type'] = 'warning'
                elif 'SUCCESS' in line.upper() or 'sucesso' in line.lower():
                    log_entry['type'] = 'success'

                log_lines.append(log_entry)

        return jsonify({
            'success': True,
            'logs': log_lines
        })

    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Timeout ao ler logs'}), 500
    except FileNotFoundError:
        # journalctl não disponível, tenta ler arquivo de log
        try:
            log_file = Path('./logs/app.log')
            if log_file.exists():
                with open(log_file, 'r') as f:
                    lines_list = f.readlines()[-int(request.args.get('lines', 50)):]
                    log_lines = [{'message': l.strip(), 'type': 'info'} for l in lines_list if l.strip()]
                    return jsonify({'success': True, 'logs': log_lines})
        except:
            pass
        return jsonify({'success': True, 'logs': [{'message': 'Sistema de logs não disponível', 'type': 'warning'}]})
    except Exception as e:
        logger.error(f"Erro ao obter logs do sistema: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/logs/clear', methods=['POST'])
@login_required
def clear_logs():
    """Limpa o histórico de logs em memória"""
    global log_history
    log_history = []
    return jsonify({'success': True, 'message': 'Logs limpos'})

# ============================================================================
# ROTAS ESTÁTICAS
# ============================================================================

@app.route('/')
@login_required
def index():
    """Serve a página principal (requer login)"""
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve arquivos estáticos"""
    # Permite acesso ao login.html sem autenticação
    if path == 'login.html':
        return send_from_directory('static', path)
    # Permite acesso a arquivos CSS/JS/imagens sem autenticação (para o login funcionar)
    if path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf')):
        return send_from_directory('static', path)
    # Outras páginas requerem login
    if not session.get('logged_in'):
        return redirect('/login')
    return send_from_directory('static', path)

# ============================================================================
# API - CONFIGURAÇÃO
# ============================================================================

@app.route('/api/config/keys', methods=['GET'])
@login_required
def get_api_keys_status():
    """Retorna status de quais API keys estão configuradas (com valores mascarados)"""
    try:
        def mask_key(key):
            """Mascara a API key mostrando apenas primeiros e últimos caracteres"""
            if not key:
                return None
            if len(key) <= 8:
                return '*' * len(key)
            return key[:4] + '*' * (len(key) - 8) + key[-4:]

        return jsonify({
            'success': True,
            'keys': {
                'elevenlabs': bool(Config.ELEVENLABS_API_KEY),
                'minimax': bool(Config.MINIMAX_API_KEY),
                'gemini': bool(Config.GEMINI_API_KEY),
                'wavespeed': bool(Config.WAVESPEED_API_KEY)
            },
            'masked_keys': {
                'elevenlabs': mask_key(Config.ELEVENLABS_API_KEY),
                'minimax': mask_key(Config.MINIMAX_API_KEY),
                'gemini': mask_key(Config.GEMINI_API_KEY),
                'wavespeed': mask_key(Config.WAVESPEED_API_KEY)
            }
        })
    except Exception as e:
        logger.error(f"Erro ao verificar API keys: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/config/keys', methods=['POST'])
@login_required
def save_api_keys():
    """Salva API keys no arquivo .env"""
    try:
        data = request.json
        
        # Validação
        if not data:
            return jsonify({'success': False, 'error': 'Nenhum dado recebido'}), 400
        
        # Lê .env atual ou cria novo
        env_path = Path('.env')
        env_content = {}
        
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_content[key.strip()] = value.strip()
        
        # Atualiza com novos valores
        if 'elevenlabs_api_key' in data and data['elevenlabs_api_key']:
            env_content['ELEVENLABS_API_KEY'] = data['elevenlabs_api_key']
        
        if 'minimax_api_key' in data and data['minimax_api_key']:
            env_content['MINIMAX_API_KEY'] = data['minimax_api_key']
        
        if 'gemini_api_key' in data and data['gemini_api_key']:
            env_content['GEMINI_API_KEY'] = data['gemini_api_key']
        
        if 'wavespeed_api_key' in data and data['wavespeed_api_key']:
            env_content['WAVESPEED_API_KEY'] = data['wavespeed_api_key']
        
        # Salva .env
        with open(env_path, 'w', encoding='utf-8') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        
        # Recarrega configuração
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        # Atualiza Config
        Config.ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
        Config.MINIMAX_API_KEY = os.getenv('MINIMAX_API_KEY')
        Config.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        Config.WAVESPEED_API_KEY = os.getenv('WAVESPEED_API_KEY')
        
        logger.info("API keys atualizadas com sucesso")
        
        return jsonify({
            'success': True,
            'message': 'API keys salvas com sucesso! As configurações foram atualizadas.'
        })
        
    except Exception as e:
        logger.error(f"Erro ao salvar API keys: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - VOZES
# ============================================================================

@app.route('/api/voices/<provider>', methods=['GET'])
@login_required
def get_voices(provider: str):
    """Retorna lista de vozes disponíveis do provedor"""
    try:
        if provider not in ['elevenlabs', 'minimax']:
            return jsonify({'success': False, 'error': 'Provedor inválido'}), 400
        
        audio_gen = AudioGenerator(provider=provider)
        voices = audio_gen.get_available_voices()
        
        if voices and len(voices) > 0:
            voice_list = [voice['name'] for voice in voices]
            return jsonify({
                'success': True,
                'voices': voice_list
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Nenhuma voz disponível. Verifique a API key do {provider}'
            }), 400
            
    except Exception as e:
        logger.error(f"Erro ao obter vozes do {provider}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - ESTIMATIVA
# ============================================================================

@app.route('/api/estimate', methods=['POST'])
def estimate_job():
    """Calcula estimativa de custo e tempo"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text or not text.strip():
            return jsonify({'success': False, 'error': 'Texto não fornecido'}), 400
        
        temp_mgr = JobManager()
        estimate = temp_mgr.get_job_estimate(text)
        
        return jsonify({
            'success': True,
            'estimate': estimate
        })
        
    except Exception as e:
        logger.error(f"Erro ao calcular estimativa: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - PREVIEW
# ============================================================================

@app.route('/api/preview', methods=['POST'])
def generate_preview():
    """Gera preview dos roteiros com batches"""
    try:
        data = request.json
        scripts_text = data.get('scripts_text', '')
        batch_size = data.get('batch_size', Config.BATCH_SIZE)

        # Valida batch_size (entre 1 e 10)
        batch_size = max(1, min(10, int(batch_size)))

        if not scripts_text or not scripts_text.strip():
            return jsonify({'success': False, 'error': 'Texto não fornecido'}), 400

        # Separa roteiros por "---"
        raw_scripts = [s.strip() for s in scripts_text.split('---') if s.strip()]

        if not raw_scripts:
            return jsonify({'success': False, 'error': 'Nenhum roteiro encontrado'}), 400

        scripts_data = []

        for idx, script in enumerate(raw_scripts, 1):
            # Divide em parágrafos
            paragraphs = split_into_paragraphs(script)

            # Cria batches usando o tamanho especificado pelo usuário
            batches = create_batches(paragraphs, batch_size)
            
            # Monta estrutura do roteiro
            script_data = {
                "id": idx,
                "text": script,
                "paragraphs": paragraphs,
                "batches": [
                    {
                        "batch_number": b_idx + 1,
                        "text": "\n\n".join(batch),
                        "char_count": sum(len(p) for p in batch),
                        "image_index": 0
                    }
                    for b_idx, batch in enumerate(batches)
                ],
                "total_chars": len(script),
                "total_batches": len(batches)
            }
            
            scripts_data.append(script_data)
        
        total_batches = sum(s["total_batches"] for s in scripts_data)
        total_chars = sum(s["total_chars"] for s in scripts_data)
        
        return jsonify({
            'success': True,
            'scripts': scripts_data,
            'summary': {
                'total_scripts': len(scripts_data),
                'total_batches': total_batches,
                'total_chars': total_chars
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao gerar preview: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - UPLOAD DE IMAGENS
# ============================================================================

@app.route('/api/upload/images', methods=['POST'])
@login_required
def upload_images():
    """Faz upload de imagens"""
    try:
        if 'images' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhuma imagem enviada'}), 400
        
        files = request.files.getlist('images')
        
        if not files or len(files) == 0:
            return jsonify({'success': False, 'error': 'Nenhuma imagem enviada'}), 400
        
        uploaded_paths = []
        
        for file in files:
            if file.filename == '':
                continue
            
            filename = secure_filename(file.filename)
            filepath = UPLOAD_FOLDER / filename
            file.save(str(filepath))
            uploaded_paths.append(str(filepath))
        
        if not uploaded_paths:
            return jsonify({'success': False, 'error': 'Nenhuma imagem válida'}), 400
        
        return jsonify({
            'success': True,
            'paths': uploaded_paths,
            'count': len(uploaded_paths)
        })
        
    except Exception as e:
        logger.error(f"Erro ao fazer upload de imagens: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - GERAÇÃO DE VÍDEOS
# ============================================================================

@app.route('/api/generate/single', methods=['POST'])
@login_required
def generate_single_video():
    """Gera um vídeo único"""
    try:
        data = request.json

        text = data.get('text', '')
        provider = data.get('provider', 'elevenlabs')
        voice_name = data.get('voice_name', '')
        model_id = data.get('model_id', 'eleven_multilingual_v2')
        image_paths = data.get('image_paths', [])
        max_workers = data.get('max_workers', 3)
        skip_formatting = data.get('skip_formatting', False)  # Pular formatação Gemini

        # Validação
        if not text or not text.strip():
            return jsonify({'success': False, 'error': 'Texto não fornecido'}), 400

        if not voice_name:
            return jsonify({'success': False, 'error': 'Voz não selecionada'}), 400

        if not image_paths or len(image_paths) == 0:
            return jsonify({'success': False, 'error': 'Nenhuma imagem fornecida'}), 400

        # Cria job manager
        job_mgr = JobManager(audio_provider=provider)

        # Cria job
        job, error = job_mgr.create_job(
            input_text=text,
            voice_name=voice_name,
            image_paths=image_paths,
            model_id=model_id,
            skip_formatting=skip_formatting
        )
        
        if error:
            return jsonify({'success': False, 'error': error}), 400
        
        # Create database job
        db_job = db.create_job({
            'type': 'single_video',
            'metadata': {'text_preview': text[:100]}
        })
        db_job_id = db_job['id']
        
        try:
            # Processa job
            final_video = job_mgr.process_job(
                job=job,
                max_workers_video=max_workers
            )
            
            # Update job as completed
            db.update_job(db_job_id, {
                'status': 'completed',
                'video_path': str(final_video)
            })
            
            duration = (job.completed_at - job.created_at).total_seconds()
            
            return jsonify({
                'success': True,
                'video_path': str(final_video),
                'job_id': job.job_id,
                'duration': duration
            })
        except Exception as process_error:
            db.update_job(db_job_id, {'status': 'failed'})
            raise process_error
        
    except Exception as e:
        logger.error(f"Erro ao gerar vídeo: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate/batch', methods=['POST'])
@login_required
def generate_batch_videos():
    """Gera múltiplos vídeos em lote"""
    try:
        data = request.json

        scripts = data.get('scripts', [])
        provider = data.get('provider', 'elevenlabs')
        model_id = data.get('model_id', 'eleven_multilingual_v2')
        image_paths = data.get('image_paths', [])
        max_workers = data.get('max_workers', 3)
        voice_selections = data.get('voice_selections', [])
        batch_image_mode = data.get('batch_image_mode', 'fixed')
        batch_images = data.get('batch_images', {})  # {scriptId_batchNumber: image_path}
        skip_formatting = data.get('skip_formatting', False)  # Pular formatação Gemini

        # Validação
        if not scripts or len(scripts) == 0:
            return jsonify({'success': False, 'error': 'Nenhum roteiro fornecido'}), 400

        if not image_paths or len(image_paths) == 0:
            return jsonify({'success': False, 'error': 'Nenhuma imagem fornecida'}), 400

        # Cria job manager
        job_mgr = JobManager(audio_provider=provider)

        results = []
        videos_gerados = []

        # Create database job for batch
        batch_job = db.create_job({
            'type': 'batch_videos',
            'metadata': {'num_scripts': len(scripts)}
        })
        batch_job_id = batch_job['id']

        for idx, script_data in enumerate(scripts):
            try:
                script_text = script_data.get('text', '')
                script_id = script_data.get('id')
                voice_name = voice_selections[idx] if idx < len(voice_selections) else voice_selections[0]

                # Determine image paths for this script based on mode
                if batch_image_mode == 'individual':
                    # Collect images for each batch in this script
                    script_image_paths = []
                    batches = script_data.get('batches', [])

                    for batch in batches:
                        batch_number = batch.get('batch_number')
                        batch_key = f"{script_id}_{batch_number}"

                        if batch_key in batch_images:
                            batch_image_path = batch_images[batch_key]
                            if batch_image_path not in script_image_paths:
                                script_image_paths.append(batch_image_path)

                    # If no specific images found, fallback to default image_paths
                    if not script_image_paths:
                        script_image_paths = image_paths
                else:
                    # Fixed mode - use the same images for all scripts
                    script_image_paths = image_paths

                # Cria job
                job, error = job_mgr.create_job(
                    input_text=script_text,
                    voice_name=voice_name,
                    image_paths=script_image_paths,
                    model_id=model_id,
                    skip_formatting=skip_formatting
                )

                if error:
                    results.append({
                        'script_id': script_id,
                        'success': False,
                        'error': error
                    })
                    continue

                # Processa job
                final_video = job_mgr.process_job(
                    job=job,
                    max_workers_video=max_workers
                )

                duration = (job.completed_at - job.created_at).total_seconds()
                videos_gerados.append(str(final_video))

                results.append({
                    'script_id': script_id,
                    'success': True,
                    'video_path': str(final_video),
                    'duration': duration
                })

            except Exception as e:
                results.append({
                    'script_id': script_data.get('id'),
                    'success': False,
                    'error': str(e)
                })

        # Update batch job as completed
        if videos_gerados:
            db.update_job(batch_job_id, {
                'status': 'completed',
                'video_path': videos_gerados[0] if len(videos_gerados) == 1 else f'{len(videos_gerados)} vídeos'
            })
        else:
            db.update_job(batch_job_id, {'status': 'failed'})

        return jsonify({
            'success': True,
            'results': results,
            'videos_count': len(videos_gerados),
            'total_scripts': len(scripts)
        })

    except Exception as e:
        logger.error(f"Erro ao gerar vídeos em lote: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - DOWNLOAD DE VÍDEO
# ============================================================================

@app.route('/api/download/<path:filename>', methods=['GET'])
def download_video(filename):
    """Faz download de vídeo gerado"""
    try:
        from urllib.parse import unquote
        # Decodifica o path que pode vir URL-encoded
        decoded_filename = unquote(filename)
        video_path = Path(decoded_filename)

        if not video_path.exists():
            return jsonify({'success': False, 'error': 'Vídeo não encontrado'}), 404

        return send_file(str(video_path), as_attachment=True, download_name=video_path.name)

    except Exception as e:
        logger.error(f"Erro ao fazer download: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stream/<path:filename>', methods=['GET'])
def stream_video(filename):
    """Stream de vídeo para visualização no navegador"""
    try:
        from urllib.parse import unquote
        # Decodifica o path que pode vir URL-encoded
        decoded_filename = unquote(filename)
        video_path = Path(decoded_filename)

        if not video_path.exists():
            return jsonify({'success': False, 'error': 'Vídeo não encontrado'}), 404

        return send_file(str(video_path), mimetype='video/mp4')

    except Exception as e:
        logger.error(f"Erro ao fazer stream: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/videos/history', methods=['GET'])
def get_video_history():
    """Lista vídeos do histórico (pasta temp e subpastas de jobs)"""
    try:
        temp_folder = Path('./temp')
        if not temp_folder.exists():
            return jsonify({'success': True, 'videos': []})

        videos = []

        # Busca em temp/outputs (legado)
        output_folder = temp_folder / 'outputs'
        if output_folder.exists():
            for video_file in output_folder.glob('*.mp4'):
                try:
                    stat = video_file.stat()
                    videos.append({
                        'name': video_file.name,
                        'path': str(video_file),
                        'size': stat.st_size,
                        'created_at': stat.st_mtime
                    })
                except Exception:
                    pass

        # Busca em pastas de jobs (temp/job_*)
        for job_dir in temp_folder.glob('job_*'):
            if job_dir.is_dir():
                # Procura final_output.mp4 ou qualquer .mp4
                for video_file in job_dir.glob('*.mp4'):
                    try:
                        stat = video_file.stat()
                        # Usa nome do job + nome do arquivo para identificação
                        display_name = f"{job_dir.name}_{video_file.name}"
                        videos.append({
                            'name': display_name,
                            'path': str(video_file),
                            'size': stat.st_size,
                            'created_at': stat.st_mtime
                        })
                    except Exception:
                        pass

        # Remove duplicatas baseado no path
        seen_paths = set()
        unique_videos = []
        for video in videos:
            if video['path'] not in seen_paths:
                seen_paths.add(video['path'])
                unique_videos.append(video)

        # Sort by creation time (newest first)
        unique_videos.sort(key=lambda x: x['created_at'], reverse=True)

        return jsonify({'success': True, 'videos': unique_videos})

    except Exception as e:
        logger.error(f"Erro ao listar histórico: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - PROJECTS
# ============================================================================

@app.route('/api/projects', methods=['GET'])
def get_projects():
    """Lista todos os projetos"""
    try:
        tag_filter = request.args.get('tag')
        projects = db.get_projects(tag_filter=tag_filter)
        
        return jsonify({
            'success': True,
            'projects': projects
        })
    except Exception as e:
        logger.error(f"Erro ao listar projetos: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects', methods=['POST'])
def create_project():
    """Cria um novo projeto"""
    try:
        data = request.json
        name = data.get('name', '')
        description = data.get('description', '')
        tags = data.get('tags', [])
        
        if not name:
            return jsonify({'success': False, 'error': 'Nome do projeto é obrigatório'}), 400
        
        project = db.create_project(name, description, tags)
        
        return jsonify({
            'success': True,
            'project': project
        })
    except Exception as e:
        logger.error(f"Erro ao criar projeto: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    """Obtém detalhes de um projeto"""
    try:
        project = db.get_project(project_id)
        
        if not project:
            return jsonify({'success': False, 'error': 'Projeto não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'project': project
        })
    except Exception as e:
        logger.error(f"Erro ao obter projeto: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Atualiza um projeto"""
    try:
        data = request.json
        project = db.update_project(project_id, data)
        
        if not project:
            return jsonify({'success': False, 'error': 'Projeto não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'project': project
        })
    except Exception as e:
        logger.error(f"Erro ao atualizar projeto: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Deleta um projeto"""
    try:
        db.delete_project(project_id)
        
        return jsonify({
            'success': True,
            'message': 'Projeto deletado com sucesso'
        })
    except Exception as e:
        logger.error(f"Erro ao deletar projeto: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/projects/<project_id>/videos', methods=['POST'])
def add_video_to_project(project_id):
    """Adiciona vídeo a um projeto"""
    try:
        data = request.json
        success = db.add_video_to_project(project_id, data)
        
        if not success:
            return jsonify({'success': False, 'error': 'Projeto não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Vídeo adicionado ao projeto'
        })
    except Exception as e:
        logger.error(f"Erro ao adicionar vídeo: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - AVATARS
# ============================================================================

@app.route('/api/avatars', methods=['GET'])
def get_avatars():
    """Lista todos os avatares"""
    try:
        avatars = db.get_avatars()
        
        return jsonify({
            'success': True,
            'avatars': avatars
        })
    except Exception as e:
        logger.error(f"Erro ao listar avatares: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/avatars', methods=['POST'])
def create_avatar():
    """Cria um novo avatar (salva imagem template)"""
    try:
        from datetime import datetime
        
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhuma imagem enviada'}), 400
        
        file = request.files['image']
        name = request.form.get('name', file.filename)
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Arquivo inválido'}), 400
        
        # Salva imagem
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        
        avatar_path = db.avatars_dir / unique_filename
        file.save(str(avatar_path))
        
        # Cria thumbnail (simplificado - usa a mesma imagem)
        thumbnail_path = db.avatars_dir / "thumbnails" / unique_filename
        file.seek(0)  # Reset file pointer
        file.save(str(thumbnail_path))
        
        # Salva no banco
        avatar = db.create_avatar(name, str(avatar_path), str(thumbnail_path))
        
        return jsonify({
            'success': True,
            'avatar': avatar
        })
    except Exception as e:
        logger.error(f"Erro ao criar avatar: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/avatars/<avatar_id>', methods=['DELETE'])
def delete_avatar(avatar_id):
    """Deleta um avatar"""
    try:
        db.delete_avatar(avatar_id)
        
        return jsonify({
            'success': True,
            'message': 'Avatar deletado com sucesso'
        })
    except Exception as e:
        logger.error(f"Erro ao deletar avatar: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/avatars/<avatar_id>/image', methods=['GET'])
def get_avatar_image(avatar_id):
    """Obtém imagem principal do avatar (primeira imagem)"""
    try:
        avatar = db.get_avatar(avatar_id)

        if not avatar:
            return jsonify({'success': False, 'error': 'Avatar não encontrado'}), 404

        # Tenta primeiro usar o novo formato (images array)
        if avatar.get('images') and len(avatar['images']) > 0:
            image_path = Path(avatar['images'][0]['path'])
        elif avatar.get('image_path'):
            image_path = Path(avatar['image_path'])
        else:
            return jsonify({'success': False, 'error': 'Imagem não encontrada'}), 404

        if not image_path.exists():
            return jsonify({'success': False, 'error': 'Imagem não encontrada'}), 404

        return send_file(str(image_path))
    except Exception as e:
        logger.error(f"Erro ao obter imagem: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/avatars/<avatar_id>/images', methods=['GET'])
def get_avatar_images(avatar_id):
    """Obtém todas as imagens de um avatar"""
    try:
        images = db.get_avatar_images(avatar_id)

        return jsonify({
            'success': True,
            'images': images
        })
    except Exception as e:
        logger.error(f"Erro ao obter imagens do avatar: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/avatars/<avatar_id>/images', methods=['POST'])
@login_required
def add_image_to_avatar(avatar_id):
    """Adiciona uma imagem a um avatar existente"""
    try:
        from datetime import datetime

        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhuma imagem enviada'}), 400

        file = request.files['image']

        if file.filename == '':
            return jsonify({'success': False, 'error': 'Arquivo inválido'}), 400

        # Verifica se avatar existe
        avatar = db.get_avatar(avatar_id)
        if not avatar:
            return jsonify({'success': False, 'error': 'Avatar não encontrado'}), 404

        # Salva imagem
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        unique_filename = f"{timestamp}_{filename}"

        image_path = db.avatars_dir / unique_filename
        file.save(str(image_path))

        # Cria thumbnail
        thumbnail_path = db.avatars_dir / "thumbnails" / unique_filename
        file.seek(0)
        file.save(str(thumbnail_path))

        # Adiciona ao avatar
        updated_avatar = db.add_image_to_avatar(avatar_id, str(image_path), str(thumbnail_path))

        if not updated_avatar:
            return jsonify({'success': False, 'error': 'Erro ao adicionar imagem'}), 500

        return jsonify({
            'success': True,
            'avatar': updated_avatar
        })
    except Exception as e:
        logger.error(f"Erro ao adicionar imagem ao avatar: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/avatars/<avatar_id>/images/<image_id>', methods=['DELETE'])
@login_required
def remove_image_from_avatar(avatar_id, image_id):
    """Remove uma imagem de um avatar"""
    try:
        updated_avatar = db.remove_image_from_avatar(avatar_id, image_id)

        if not updated_avatar:
            return jsonify({'success': False, 'error': 'Avatar ou imagem não encontrado'}), 404

        return jsonify({
            'success': True,
            'avatar': updated_avatar
        })
    except Exception as e:
        logger.error(f"Erro ao remover imagem do avatar: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/avatars/<avatar_id>/images/<image_id>/file', methods=['GET'])
def get_avatar_image_file(avatar_id, image_id):
    """Obtém arquivo de uma imagem específica do avatar"""
    try:
        avatar = db.get_avatar(avatar_id)

        if not avatar:
            return jsonify({'success': False, 'error': 'Avatar não encontrado'}), 404

        # Procura a imagem pelo ID
        for img in avatar.get('images', []):
            if img['id'] == image_id:
                image_path = Path(img['path'])
                if image_path.exists():
                    return send_file(str(image_path))
                else:
                    return jsonify({'success': False, 'error': 'Arquivo não encontrado'}), 404

        return jsonify({'success': False, 'error': 'Imagem não encontrada'}), 404
    except Exception as e:
        logger.error(f"Erro ao obter arquivo de imagem: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - JOBS (Timeline de processamento)
# ============================================================================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Lista jobs (timeline de processamento)"""
    try:
        status = request.args.get('status')  # processing, completed, failed
        limit = int(request.args.get('limit', 50))
        
        jobs = db.get_jobs(status=status, limit=limit)
        
        return jsonify({
            'success': True,
            'jobs': jobs
        })
    except Exception as e:
        logger.error(f"Erro ao listar jobs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
    """Obtém status de um job específico"""
    try:
        job = db.get_job(job_id)
        
        if not job:
            return jsonify({'success': False, 'error': 'Job não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'job': job
        })
    except Exception as e:
        logger.error(f"Erro ao obter job: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - TAGS
# ============================================================================

@app.route('/api/tags', methods=['GET'])
def get_tags():
    """Lista todas as tags"""
    try:
        tags = db.get_tags()
        
        return jsonify({
            'success': True,
            'tags': tags
        })
    except Exception as e:
        logger.error(f"Erro ao listar tags: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tags', methods=['POST'])
def create_tag():
    """Cria uma nova tag"""
    try:
        data = request.json
        name = data.get('name', '')
        color = data.get('color', '#667eea')
        
        if not name:
            return jsonify({'success': False, 'error': 'Nome da tag é obrigatório'}), 400
        
        tag = db.create_tag(name, color)
        
        return jsonify({
            'success': True,
            'tag': tag
        })
    except Exception as e:
        logger.error(f"Erro ao criar tag: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tags/<tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    """Deleta uma tag"""
    try:
        db.delete_tag(tag_id)

        return jsonify({
            'success': True,
            'message': 'Tag deletada com sucesso'
        })
    except Exception as e:
        logger.error(f"Erro ao deletar tag: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# API - GEMINI AI (Seleção Automática de Imagens)
# ============================================================================

@app.route('/api/gemini/select-images', methods=['POST'])
@login_required
def gemini_select_images():
    """
    Usa Gemini para selecionar automaticamente a melhor imagem para cada batch.
    Recebe os batches (textos) e as imagens disponíveis, retorna mapeamento batch->imagem.
    """
    try:
        import google.generativeai as genai
        import base64

        data = request.json
        batches = data.get('batches', [])  # [{script_id, batch_number, text}, ...]
        avatar_id = data.get('avatar_id')

        if not batches:
            return jsonify({'success': False, 'error': 'Nenhum batch fornecido'}), 400

        if not avatar_id:
            return jsonify({'success': False, 'error': 'Avatar não especificado'}), 400

        # Obtém imagens do avatar
        avatar = db.get_avatar(avatar_id)
        if not avatar:
            return jsonify({'success': False, 'error': 'Avatar não encontrado'}), 404

        images = avatar.get('images', [])
        if not images or len(images) == 0:
            return jsonify({'success': False, 'error': 'Avatar não possui imagens'}), 400

        # Configura Gemini
        if not Config.GEMINI_API_KEY:
            return jsonify({'success': False, 'error': 'API key do Gemini não configurada'}), 400

        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Prepara descrição das imagens
        image_descriptions = []
        for i, img in enumerate(images):
            image_descriptions.append(f"Imagem {i+1} (ID: {img['id']})")

        # Prepara lista de batches
        batch_texts = []
        for batch in batches:
            batch_key = f"{batch['script_id']}_{batch['batch_number']}"
            batch_texts.append(f"Batch {batch_key}: {batch['text'][:500]}...")

        # Cria prompt para o Gemini
        prompt = f"""Você é um assistente de produção de vídeo. Analise os textos dos batches abaixo e as imagens disponíveis do avatar.

Para cada batch, escolha a imagem mais adequada baseando-se no tom e conteúdo do texto:
- Textos mais sérios/formais: escolha imagens com expressão mais neutra
- Textos alegres/entusiasmados: escolha imagens com sorriso
- Textos explicativos: escolha imagens com expressão atenta
- Textos de venda/persuasão: escolha imagens confiantes

Imagens disponíveis:
{chr(10).join(image_descriptions)}

Textos dos batches:
{chr(10).join(batch_texts)}

Responda APENAS com um JSON no formato:
{{"selections": {{"script_id_batch_number": "image_id", ...}}}}

Exemplo de resposta:
{{"selections": {{"1_1": "img_abc123", "1_2": "img_def456", "2_1": "img_abc123"}}}}

Se houver apenas uma imagem, use a mesma para todos os batches."""

        # Chama Gemini
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Tenta extrair JSON da resposta
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            selections = result.get('selections', {})

            # Converte para o formato esperado (batch_key -> image_path)
            batch_images = {}
            for batch_key, image_id in selections.items():
                # Encontra o path da imagem pelo ID
                for img in images:
                    if img['id'] == image_id:
                        batch_images[batch_key] = img['path']
                        break
                # Se não encontrou, usa a primeira imagem
                if batch_key not in batch_images and images:
                    batch_images[batch_key] = images[0]['path']

            return jsonify({
                'success': True,
                'batch_images': batch_images,
                'gemini_response': response_text
            })
        else:
            # Fallback: usa a primeira imagem para todos
            batch_images = {}
            for batch in batches:
                batch_key = f"{batch['script_id']}_{batch['batch_number']}"
                batch_images[batch_key] = images[0]['path']

            return jsonify({
                'success': True,
                'batch_images': batch_images,
                'fallback': True,
                'message': 'Não foi possível interpretar resposta do Gemini, usando primeira imagem'
            })

    except ImportError:
        return jsonify({'success': False, 'error': 'Biblioteca google-generativeai não instalada'}), 500
    except Exception as e:
        logger.error(f"Erro na seleção automática com Gemini: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  LipSync Video Generator - Web Interface")
    print("="*60)
    print("\n  Interface web moderna com configuração de API keys integrada")
    print(f"\n  🌐 Acesse: http://localhost:5000")
    print(f"  📁 Pasta de uploads: {UPLOAD_FOLDER}")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
