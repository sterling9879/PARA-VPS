"""
Script de setup para criar assets iniciais (avatares e templates)
"""
from pathlib import Path
from project_manager import ProjectManager
import shutil

def create_sample_avatars(project_manager: ProjectManager):
    """Cria avatares de exemplo"""
    print("📷 Criando biblioteca de avatares...")

    # Cria arquivos placeholder para avatares
    avatars_info = [
        ("João Silva", "male", "Avatar masculino profissional"),
        ("Carlos Costa", "male", "Avatar masculino casual"),
        ("Pedro Santos", "male", "Avatar masculino executivo"),
        ("Maria Oliveira", "female", "Avatar feminino profissional"),
        ("Ana Paula", "female", "Avatar feminino casual"),
        ("Julia Ferreira", "female", "Avatar feminino executiva"),
    ]

    for name, category, desc in avatars_info:
        # Cria arquivo placeholder (na produção, use imagens reais)
        avatar_dir = project_manager.avatars_dir / category
        avatar_id = f"{category}_{len([f for f in avatar_dir.glob('*.txt')]) + 1}"
        placeholder_file = avatar_dir / f"{avatar_id}.txt"

        with open(placeholder_file, 'w') as f:
            f.write(f"Avatar: {name}\nCategoria: {category}\nDescrição: {desc}\n")

        print(f"  ✅ Avatar criado: {name} ({category})")

    print(f"✅ {len(avatars_info)} avatares criados!\n")

def create_sample_templates(project_manager: ProjectManager):
    """Cria templates de exemplo"""
    print("📝 Criando templates de vídeo...")

    templates = [
        {
            "name": "Vídeo Educacional",
            "script": """Olá! Bem-vindo ao nosso canal educacional.

Hoje vamos explorar um tema fascinante que vai transformar sua compreensão sobre o assunto.

Prepare-se para uma jornada de aprendizado incrível!""",
            "voice": "Rachel",
            "provider": "elevenlabs",
            "model": "eleven_multilingual_v3"
        },
        {
            "name": "Apresentação de Produto",
            "script": """Apresentamos o produto revolucionário que vai mudar sua vida.

Com tecnologia de ponta e design inovador, este produto oferece benefícios únicos.

Descubra como ele pode fazer a diferença para você!""",
            "voice": "Adam",
            "provider": "elevenlabs",
            "model": "eleven_multilingual_v3"
        },
        {
            "name": "Tutorial Rápido",
            "script": """Neste tutorial rápido, você vai aprender o passo a passo completo.

Siga as instruções com atenção e em poucos minutos você estará dominando a técnica.

Vamos começar!""",
            "voice": "Domi",
            "provider": "elevenlabs",
            "model": "eleven_turbo_v3"
        },
        {
            "name": "Notícia/Informativo",
            "script": """Bom dia! Aqui estão as principais notícias do dia.

Hoje trazemos informações relevantes sobre os acontecimentos mais importantes.

Fique por dentro de tudo que está acontecendo!""",
            "voice": "Bella",
            "provider": "elevenlabs",
            "model": "eleven_flash_v3"
        },
        {
            "name": "Motivacional",
            "script": """Você tem um potencial incrível dentro de você!

Cada dia é uma nova oportunidade para alcançar seus sonhos e superar seus limites.

Acredite em si mesmo e siga em frente com determinação!""",
            "voice": "Josh",
            "provider": "elevenlabs",
            "model": "eleven_multilingual_v3"
        }
    ]

    for template in templates:
        project_manager.create_template(
            name=template["name"],
            script=template["script"],
            voice=template["voice"],
            provider=template["provider"],
            model=template.get("model")
        )
        print(f"  ✅ Template criado: {template['name']}")

    print(f"✅ {len(templates)} templates criados!\n")

def create_sample_projects(project_manager: ProjectManager):
    """Cria projetos de exemplo"""
    print("📁 Criando projetos de exemplo...")

    projects = [
        ("Vídeos Educacionais", "Série de vídeos para ensino e educação"),
        ("Marketing Digital", "Conteúdo para campanhas de marketing"),
        ("Tutoriais", "Vídeos tutoriais e how-to"),
    ]

    for name, desc in projects:
        project_manager.create_project(name, desc)
        print(f"  ✅ Projeto criado: {name}")

    print(f"✅ {len(projects)} projetos criados!\n")

def setup_complete_system():
    """Setup completo do sistema"""
    print("🚀 Iniciando setup do LipSync Video Generator Pro...\n")

    # Inicializa project manager
    project_manager = ProjectManager()

    # Cria assets
    create_sample_avatars(project_manager)
    create_sample_templates(project_manager)
    create_sample_projects(project_manager)

    print("=" * 60)
    print("✅ SETUP CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("\nO sistema está pronto para uso!")
    print("\nPróximos passos:")
    print("  1. Execute: python app_pro.py")
    print("  2. Acesse: http://localhost:7860")
    print("  3. Explore o Dashboard e comece a criar vídeos!\n")

if __name__ == "__main__":
    setup_complete_system()
