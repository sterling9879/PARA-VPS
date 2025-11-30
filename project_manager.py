"""
Sistema de Gerenciamento de Projetos e Biblioteca de Assets
"""
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from utils import get_logger

logger = get_logger(__name__)


class ProjectManager:
    """Gerencia projetos, avatares e templates"""

    def __init__(self, base_dir: Path = None):
        """
        Inicializa o gerenciador de projetos

        Args:
            base_dir: Diretório base para projetos
        """
        self.base_dir = base_dir or Path('./projects')
        self.avatars_dir = self.base_dir / 'avatars'
        self.templates_dir = self.base_dir / 'templates'
        self.outputs_dir = self.base_dir / 'outputs'

        # Cria estrutura de diretórios
        self._init_directories()

        # Carrega metadados
        self.metadata_file = self.base_dir / 'metadata.json'
        self.metadata = self._load_metadata()

        logger.info(f"ProjectManager inicializado em {self.base_dir}")

    def _init_directories(self):
        """Cria estrutura de diretórios"""
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.avatars_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

        # Cria subdiretórios de avatares
        (self.avatars_dir / 'male').mkdir(exist_ok=True)
        (self.avatars_dir / 'female').mkdir(exist_ok=True)
        (self.avatars_dir / 'custom').mkdir(exist_ok=True)

    def _load_metadata(self) -> Dict:
        """Carrega metadados do arquivo JSON"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'projects': {},
            'avatars': {},
            'templates': {},
            'stats': {
                'total_videos': 0,
                'total_duration': 0,
                'total_chars': 0
            }
        }

    def _save_metadata(self):
        """Salva metadados no arquivo JSON"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

    def create_project(self, name: str, description: str = "") -> Dict:
        """
        Cria um novo projeto

        Args:
            name: Nome do projeto
            description: Descrição do projeto

        Returns:
            Dict com informações do projeto criado
        """
        project_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_dir = self.outputs_dir / f"{project_id}_{name.replace(' ', '_')}"
        project_dir.mkdir(parents=True, exist_ok=True)

        project = {
            'id': project_id,
            'name': name,
            'description': description,
            'created_at': datetime.now().isoformat(),
            'path': str(project_dir),
            'videos': [],
            'status': 'active'
        }

        self.metadata['projects'][project_id] = project
        self._save_metadata()

        logger.info(f"Projeto criado: {name} ({project_id})")
        return project

    def list_projects(self) -> List[Dict]:
        """Lista todos os projetos"""
        return list(self.metadata['projects'].values())

    def get_project(self, project_id: str) -> Optional[Dict]:
        """Obtém informações de um projeto"""
        return self.metadata['projects'].get(project_id)

    def add_avatar(self, name: str, category: str, image_path: str) -> Dict:
        """
        Adiciona um avatar à biblioteca

        Args:
            name: Nome do avatar
            category: Categoria (male, female, custom)
            image_path: Caminho da imagem

        Returns:
            Dict com informações do avatar
        """
        avatar_id = f"{category}_{len(self.metadata['avatars']) + 1}"
        dest_dir = self.avatars_dir / category
        dest_path = dest_dir / f"{avatar_id}.png"

        # Copia imagem
        shutil.copy2(image_path, dest_path)

        avatar = {
            'id': avatar_id,
            'name': name,
            'category': category,
            'path': str(dest_path),
            'added_at': datetime.now().isoformat()
        }

        self.metadata['avatars'][avatar_id] = avatar
        self._save_metadata()

        logger.info(f"Avatar adicionado: {name} ({avatar_id})")
        return avatar

    def list_avatars(self, category: str = None) -> List[Dict]:
        """
        Lista avatares da biblioteca

        Args:
            category: Filtrar por categoria (opcional)

        Returns:
            Lista de avatares
        """
        avatars = list(self.metadata['avatars'].values())
        if category:
            avatars = [a for a in avatars if a['category'] == category]
        return avatars

    def create_template(self, name: str, script: str, voice: str, provider: str, model: str = None) -> Dict:
        """
        Cria um template de vídeo

        Args:
            name: Nome do template
            script: Roteiro do template
            voice: Voz padrão
            provider: Provedor de áudio
            model: Modelo de voz (opcional)

        Returns:
            Dict com informações do template
        """
        template_id = f"template_{len(self.metadata['templates']) + 1}"

        template = {
            'id': template_id,
            'name': name,
            'script': script,
            'voice': voice,
            'provider': provider,
            'model': model,
            'created_at': datetime.now().isoformat(),
            'uses': 0
        }

        self.metadata['templates'][template_id] = template
        self._save_metadata()

        logger.info(f"Template criado: {name} ({template_id})")
        return template

    def list_templates(self) -> List[Dict]:
        """Lista todos os templates"""
        return list(self.metadata['templates'].values())

    def get_template(self, template_id: str) -> Optional[Dict]:
        """Obtém informações de um template"""
        return self.metadata['templates'].get(template_id)

    def add_video_to_project(self, project_id: str, video_info: Dict):
        """
        Adiciona vídeo a um projeto

        Args:
            project_id: ID do projeto
            video_info: Informações do vídeo gerado
        """
        if project_id in self.metadata['projects']:
            self.metadata['projects'][project_id]['videos'].append(video_info)
            self._save_metadata()

    def update_stats(self, chars: int, duration: float):
        """
        Atualiza estatísticas globais

        Args:
            chars: Número de caracteres processados
            duration: Duração em segundos
        """
        self.metadata['stats']['total_videos'] += 1
        self.metadata['stats']['total_chars'] += chars
        self.metadata['stats']['total_duration'] += duration
        self._save_metadata()

    def get_stats(self) -> Dict:
        """Retorna estatísticas globais"""
        return self.metadata['stats']

    def get_recent_videos(self, limit: int = 10) -> List[Dict]:
        """
        Retorna vídeos recentes de todos os projetos

        Args:
            limit: Número máximo de vídeos

        Returns:
            Lista de vídeos recentes
        """
        all_videos = []
        for project in self.metadata['projects'].values():
            for video in project['videos']:
                video['project_name'] = project['name']
                all_videos.append(video)

        # Ordena por data (mais recente primeiro)
        all_videos.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        return all_videos[:limit]
