"""
Database Layer - JSON-based storage for projects, avatars, and jobs
Simple, lightweight, and sufficient for the application needs
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

class Database:
    """Simple JSON-based database"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Database files
        self.projects_file = self.data_dir / "projects.json"
        self.avatars_file = self.data_dir / "avatars.json"
        self.jobs_file = self.data_dir / "jobs.json"
        self.tags_file = self.data_dir / "tags.json"
        
        # Avatar storage directories
        self.avatars_dir = self.data_dir / "avatars"
        self.avatars_dir.mkdir(exist_ok=True)
        (self.avatars_dir / "thumbnails").mkdir(exist_ok=True)
        
        # Initialize files if they don't exist
        self._initialize_files()
    
    def _initialize_files(self):
        """Create database files if they don't exist"""
        if not self.projects_file.exists():
            self._save_json(self.projects_file, [])
        
        if not self.avatars_file.exists():
            self._save_json(self.avatars_file, [])
        
        if not self.jobs_file.exists():
            self._save_json(self.jobs_file, [])
        
        if not self.tags_file.exists():
            # Create default tags
            default_tags = [
                {"id": "tag_1", "name": "Marketing", "color": "#667eea"},
                {"id": "tag_2", "name": "Education", "color": "#43e97b"},
                {"id": "tag_3", "name": "Entertainment", "color": "#f093fb"},
            ]
            self._save_json(self.tags_file, default_tags)
    
    def _load_json(self, file_path: Path) -> Any:
        """Load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return [] if file_path.suffix == '.json' else {}
    
    def _save_json(self, file_path: Path, data: Any):
        """Save JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    # ========================================================================
    # PROJECTS
    # ========================================================================
    
    def create_project(self, name: str, description: str = "", tags: List[str] = None) -> Dict:
        """Create a new project"""
        projects = self._load_json(self.projects_file)
        
        project = {
            "id": f"proj_{uuid.uuid4().hex[:8]}",
            "name": name,
            "description": description,
            "tags": tags or [],
            "videos": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        projects.append(project)
        self._save_json(self.projects_file, projects)
        
        return project
    
    def get_projects(self, tag_filter: str = None) -> List[Dict]:
        """Get all projects, optionally filtered by tag"""
        projects = self._load_json(self.projects_file)
        
        if tag_filter:
            projects = [p for p in projects if tag_filter in p.get('tags', [])]
        
        # Sort by updated_at descending
        projects.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        
        return projects
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """Get a specific project"""
        projects = self._load_json(self.projects_file)
        
        for project in projects:
            if project['id'] == project_id:
                return project
        
        return None
    
    def update_project(self, project_id: str, updates: Dict) -> Optional[Dict]:
        """Update a project"""
        projects = self._load_json(self.projects_file)
        
        for i, project in enumerate(projects):
            if project['id'] == project_id:
                project.update(updates)
                project['updated_at'] = datetime.now().isoformat()
                projects[i] = project
                self._save_json(self.projects_file, projects)
                return project
        
        return None
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project"""
        projects = self._load_json(self.projects_file)
        
        projects = [p for p in projects if p['id'] != project_id]
        self._save_json(self.projects_file, projects)
        
        return True
    
    def add_video_to_project(self, project_id: str, video_data: Dict) -> bool:
        """Add a video to a project"""
        projects = self._load_json(self.projects_file)
        
        for i, project in enumerate(projects):
            if project['id'] == project_id:
                if 'videos' not in project:
                    project['videos'] = []
                
                video_entry = {
                    "id": f"vid_{uuid.uuid4().hex[:8]}",
                    "path": video_data.get('path'),
                    "name": video_data.get('name', 'Untitled'),
                    "duration": video_data.get('duration', 0),
                    "created_at": datetime.now().isoformat()
                }
                
                project['videos'].append(video_entry)
                project['updated_at'] = datetime.now().isoformat()
                projects[i] = project
                self._save_json(self.projects_file, projects)
                
                return True
        
        return False
    
    # ========================================================================
    # AVATARS
    # ========================================================================

    def create_avatar(self, name: str, image_path: str = None, thumbnail_path: str = None, images: List[Dict] = None) -> Dict:
        """Create a new avatar entry with multiple images support"""
        avatars = self._load_json(self.avatars_file)

        avatar = {
            "id": f"avatar_{uuid.uuid4().hex[:8]}",
            "name": name,
            "images": images or [],
            "thumbnail_path": thumbnail_path or (image_path if image_path else None),
            "created_at": datetime.now().isoformat()
        }

        # Se foi passado image_path (compatibilidade), adiciona como primeira imagem
        if image_path:
            avatar["images"].append({
                "id": f"img_{uuid.uuid4().hex[:8]}",
                "path": image_path,
                "thumbnail": thumbnail_path or image_path
            })

        avatars.append(avatar)
        self._save_json(self.avatars_file, avatars)

        return avatar

    def add_image_to_avatar(self, avatar_id: str, image_path: str, thumbnail_path: str = None) -> Optional[Dict]:
        """Add an image to an existing avatar"""
        avatars = self._load_json(self.avatars_file)

        for i, avatar in enumerate(avatars):
            if avatar['id'] == avatar_id:
                if 'images' not in avatar:
                    avatar['images'] = []

                image_entry = {
                    "id": f"img_{uuid.uuid4().hex[:8]}",
                    "path": image_path,
                    "thumbnail": thumbnail_path or image_path
                }

                avatar['images'].append(image_entry)

                # Se for a primeira imagem, define como thumbnail principal
                if len(avatar['images']) == 1:
                    avatar['thumbnail_path'] = thumbnail_path or image_path

                avatars[i] = avatar
                self._save_json(self.avatars_file, avatars)
                return avatar

        return None

    def remove_image_from_avatar(self, avatar_id: str, image_id: str) -> Optional[Dict]:
        """Remove an image from an avatar"""
        avatars = self._load_json(self.avatars_file)

        for i, avatar in enumerate(avatars):
            if avatar['id'] == avatar_id:
                if 'images' in avatar:
                    # Remove a imagem e seus arquivos
                    for img in avatar['images']:
                        if img['id'] == image_id:
                            try:
                                Path(img['path']).unlink(missing_ok=True)
                                if img.get('thumbnail'):
                                    Path(img['thumbnail']).unlink(missing_ok=True)
                            except Exception as e:
                                print(f"Error deleting image files: {e}")

                    avatar['images'] = [img for img in avatar['images'] if img['id'] != image_id]

                    # Atualiza thumbnail principal se necessário
                    if avatar['images']:
                        avatar['thumbnail_path'] = avatar['images'][0].get('thumbnail') or avatar['images'][0].get('path')
                    else:
                        avatar['thumbnail_path'] = None

                    avatars[i] = avatar
                    self._save_json(self.avatars_file, avatars)
                return avatar

        return None

    def get_avatar_images(self, avatar_id: str) -> List[Dict]:
        """Get all images for an avatar"""
        avatar = self.get_avatar(avatar_id)
        if avatar:
            return avatar.get('images', [])
        return []

    def get_avatars(self) -> List[Dict]:
        """Get all avatars"""
        avatars = self._load_json(self.avatars_file)

        # Migração: converte avatars antigos para novo formato
        updated = False
        for avatar in avatars:
            if 'images' not in avatar:
                avatar['images'] = []
                if avatar.get('image_path'):
                    avatar['images'].append({
                        "id": f"img_{uuid.uuid4().hex[:8]}",
                        "path": avatar['image_path'],
                        "thumbnail": avatar.get('thumbnail_path', avatar['image_path'])
                    })
                updated = True

        if updated:
            self._save_json(self.avatars_file, avatars)

        avatars.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        return avatars

    def get_avatar(self, avatar_id: str) -> Optional[Dict]:
        """Get a specific avatar"""
        avatars = self._load_json(self.avatars_file)

        for avatar in avatars:
            if avatar['id'] == avatar_id:
                # Migração: converte avatar antigo para novo formato
                if 'images' not in avatar:
                    avatar['images'] = []
                    if avatar.get('image_path'):
                        avatar['images'].append({
                            "id": f"img_{uuid.uuid4().hex[:8]}",
                            "path": avatar['image_path'],
                            "thumbnail": avatar.get('thumbnail_path', avatar['image_path'])
                        })
                return avatar

        return None

    def delete_avatar(self, avatar_id: str) -> bool:
        """Delete an avatar and all its images"""
        avatars = self._load_json(self.avatars_file)

        # Find and delete avatar files
        for avatar in avatars:
            if avatar['id'] == avatar_id:
                # Delete all images
                for img in avatar.get('images', []):
                    try:
                        Path(img['path']).unlink(missing_ok=True)
                        if img.get('thumbnail'):
                            Path(img['thumbnail']).unlink(missing_ok=True)
                    except Exception as e:
                        print(f"Error deleting image files: {e}")

                # Delete old format image if exists
                if avatar.get('image_path'):
                    try:
                        Path(avatar['image_path']).unlink(missing_ok=True)
                        if avatar.get('thumbnail_path'):
                            Path(avatar['thumbnail_path']).unlink(missing_ok=True)
                    except Exception as e:
                        print(f"Error deleting avatar files: {e}")

        avatars = [a for a in avatars if a['id'] != avatar_id]
        self._save_json(self.avatars_file, avatars)

        return True
    
    # ========================================================================
    # JOBS
    # ========================================================================
    
    def create_job(self, job_data: Dict) -> Dict:
        """Create a job entry"""
        jobs = self._load_json(self.jobs_file)
        
        job = {
            "id": job_data.get('id', f"job_{uuid.uuid4().hex[:8]}"),
            "type": job_data.get('type', 'video_generation'),
            "status": "processing",  # processing, completed, failed
            "progress": 0,
            "estimated_time": job_data.get('estimated_time', 0),
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "video_path": None,
            "project_id": job_data.get('project_id'),
            "metadata": job_data.get('metadata', {})
        }
        
        jobs.append(job)
        self._save_json(self.jobs_file, jobs)
        
        return job
    
    def update_job(self, job_id: str, updates: Dict) -> Optional[Dict]:
        """Update a job"""
        jobs = self._load_json(self.jobs_file)
        
        for i, job in enumerate(jobs):
            if job['id'] == job_id:
                job.update(updates)
                
                if updates.get('status') == 'completed':
                    job['completed_at'] = datetime.now().isoformat()
                    job['progress'] = 100
                
                jobs[i] = job
                self._save_json(self.jobs_file, jobs)
                return job
        
        return None
    
    def get_jobs(self, status: str = None, limit: int = 50) -> List[Dict]:
        """Get jobs, optionally filtered by status"""
        jobs = self._load_json(self.jobs_file)
        
        if status:
            jobs = [j for j in jobs if j.get('status') == status]
        
        # Sort by started_at descending
        jobs.sort(key=lambda x: x.get('started_at', ''), reverse=True)
        
        return jobs[:limit]
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        """Get a specific job"""
        jobs = self._load_json(self.jobs_file)
        
        for job in jobs:
            if job['id'] == job_id:
                return job
        
        return None
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job"""
        jobs = self._load_json(self.jobs_file)
        jobs = [j for j in jobs if j['id'] != job_id]
        self._save_json(self.jobs_file, jobs)
        return True
    
    # ========================================================================
    # TAGS
    # ========================================================================
    
    def create_tag(self, name: str, color: str = "#667eea") -> Dict:
        """Create a new tag"""
        tags = self._load_json(self.tags_file)
        
        tag = {
            "id": f"tag_{uuid.uuid4().hex[:8]}",
            "name": name,
            "color": color
        }
        
        tags.append(tag)
        self._save_json(self.tags_file, tags)
        
        return tag
    
    def get_tags(self) -> List[Dict]:
        """Get all tags"""
        tags = self._load_json(self.tags_file)
        tags.sort(key=lambda x: x.get('name', ''))
        return tags
    
    def delete_tag(self, tag_id: str) -> bool:
        """Delete a tag"""
        tags = self._load_json(self.tags_file)
        tags = [t for t in tags if t['id'] != tag_id]
        self._save_json(self.tags_file, tags)
        return True


# Global database instance
db = Database()
