"""
Setup Vault Sync Script for Platinum Tier AI Employee
Initializes Git repository and configures sync for Cloud/Local agents
"""
import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    """Setup vault sync for Platinum Tier"""
    print("=" * 60)
    print("AI Employee Platinum Tier - Vault Sync Setup")
    print("=" * 60)
    print()
    
    # Get deployment mode
    print("Select deployment mode:")
    print("1. Cloud Agent (Railway)")
    print("2. Local Agent (Your Machine)")
    choice = input("Enter choice (1 or 2): ").strip()
    
    deployment_mode = 'cloud' if choice == '1' else 'local'
    agent_name = input(f"Enter agent name (e.g., {deployment_mode}-primary): ").strip()
    
    if not agent_name:
        agent_name = f"{deployment_mode}-primary"
    
    print()
    print(f"Deployment Mode: {deployment_mode}")
    print(f"Agent Name: {agent_name}")
    print()
    
    # Get Git remote URL
    print("Git Repository Setup:")
    print("Enter your Git repository URL (GitHub/GitLab/Bitbucket)")
    print("This will be used to sync between Cloud and Local agents")
    print()
    remote_url = input("Git remote URL (or press Enter to skip): ").strip()
    
    # Initialize Git
    print()
    print("Initializing Git repository...")
    
    try:
        # Check if already initialized
        git_dir = project_root / '.git'
        if not git_dir.exists():
            subprocess.run(
                ['git', 'init'],
                cwd=str(project_root),
                capture_output=True,
                check=True
            )
            print("✓ Git repository initialized")
        else:
            print("✓ Git repository already exists")
        
        # Configure Git user
        subprocess.run(
            ['git', 'config', 'user.name', f'AI-Employee-{agent_name}'],
            cwd=str(project_root),
            capture_output=True,
            check=True
        )
        subprocess.run(
            ['git', 'config', 'user.email', f'{agent_name}@ai-employee.local'],
            cwd=str(project_root),
            capture_output=True,
            check=True
        )
        print("✓ Git user configured")
        
        # Add remote if provided
        if remote_url:
            try:
                subprocess.run(
                    ['git', 'remote', 'remove', 'origin'],
                    cwd=str(project_root),
                    capture_output=True
                )
            except:
                pass
            
            subprocess.run(
                ['git', 'remote', 'add', 'origin', remote_url],
                cwd=str(project_root),
                capture_output=True,
                check=True
            )
            print(f"✓ Remote added: {remote_url}")
        
        # Create .gitignore
        create_gitignore()
        print("✓ .gitignore created (secrets excluded)")
        
        # Create sync configuration
        create_sync_config(deployment_mode, agent_name)
        print("✓ Sync configuration created")
        
        # Create required directories
        create_directories()
        print("✓ Required directories created")
        
        # Initial commit
        print()
        print("Creating initial commit...")
        subprocess.run(
            ['git', 'add', '.'],
            cwd=str(project_root),
            capture_output=True
        )
        subprocess.run(
            ['git', 'commit', '-m', 'Initial commit: Platinum Tier vault sync setup'],
            cwd=str(project_root),
            capture_output=True
        )
        print("✓ Initial commit created")
        
        # Push to remote if URL provided
        if remote_url:
            print()
            print("Pushing to remote...")
            result = subprocess.run(
                ['git', 'push', '-u', 'origin', 'main'],
                cwd=str(project_root),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✓ Pushed to remote successfully")
            else:
                print(f"⚠ Push failed: {result.stderr}")
                print("  You can push manually with: git push -u origin main")
        
        print()
        print("=" * 60)
        print("Vault Sync Setup Complete!")
        print("=" * 60)
        print()
        print("Next Steps:")
        if deployment_mode == 'cloud':
            print("1. Deploy to Railway:")
            print("   railway up")
            print()
            print("2. Set environment variables on Railway:")
            print("   - DEPLOYMENT_MODE=cloud")
            print("   - CLOUD_AGENT_NAME=" + agent_name)
            print("   - API credentials (Gmail, Meta)")
        else:
            print("1. Configure .env.local with your credentials")
            print("2. Start Local Agent:")
            print("   python3 main.py")
            print()
            print("3. Pull Cloud updates:")
            print("   git pull origin main")
        
        print()
        print("=" * 60)
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e.stderr.decode() if e.stderr else str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


def create_gitignore():
    """Create .gitignore to exclude secrets"""
    gitignore_content = """# NEVER sync these files - SECURITY CRITICAL
.env
.env.local
.env.cloud
*.env
*.token
*.session
sessions/
secure/
credentials/
keychain/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/

# Logs
logs/*.log
*.log

# OS
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temporary files
tmp/
temp/
*.tmp

# Sync folders (content syncs, but not secrets)
updates/*
!updates/.gitkeep
signals/*
!signals/.gitkeep
"""
    gitignore_file = project_root / '.gitignore'
    gitignore_file.write_text(gitignore_content, encoding='utf-8')


def create_sync_config(deployment_mode: str, agent_name: str):
    """Create sync configuration file"""
    config = {
        "deployment_mode": deployment_mode,
        "agent_name": agent_name,
        "sync_branch": "main",
        "sync_interval_seconds": 60,
        "folders": {
            "updates": "updates/",
            "signals": "signals/",
            "in_progress": "in_progress/",
            "done": "done/"
        },
        "rules": {
            "cloud_writes": ["updates/", "signals/"],
            "local_writes": ["dashboard.md", "done/"],
            "single_writer": "dashboard.md",
            "claim_by_move": "in_progress/<agent>/"
        }
    }
    
    import json
    config_file = project_root / 'sync_config.json'
    config_file.write_text(json.dumps(config, indent=2), encoding='utf-8')


def create_directories():
    """Create required directories"""
    directories = [
        'updates',
        'signals',
        'in_progress',
        'done',
        'pending_approval',
        'approved',
        'rejected',
        'needs_action',
        'plans',
        'logs',
        'logs/audit',
        'logs/signals_archive'
    ]
    
    for dir_name in directories:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep for empty directories
        gitkeep = dir_path / '.gitkeep'
        if not gitkeep.exists():
            gitkeep.write_text("")


if __name__ == "__main__":
    main()
