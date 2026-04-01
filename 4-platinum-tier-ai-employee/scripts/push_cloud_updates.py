"""
Push Cloud Updates Script for Platinum Tier AI Employee
Pushes Cloud agent drafts to Git for Local sync
"""
import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    """Push Cloud updates to Git"""
    print("=" * 60)
    print("Pushing Cloud Updates...")
    print("=" * 60)
    print()
    
    # Check if Git is initialized
    git_dir = project_root / '.git'
    if not git_dir.exists():
        print("✗ Git repository not initialized")
        print("Run: python3 scripts/setup_vault_sync.py")
        sys.exit(1)
    
    # Stage updates and signals
    print("Staging updates and signals...")
    subprocess.run(
        ['git', 'add', 'updates/', 'signals/'],
        cwd=str(project_root),
        capture_output=True
    )
    
    # Check for changes
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )
    
    if not result.stdout.strip():
        print("✓ No changes to push")
        return
    
    # Commit changes
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print("Committing changes...")
    subprocess.run(
        ['git', 'commit', '-m', f'Cloud updates: {timestamp}'],
        cwd=str(project_root),
        capture_output=True
    )
    
    # Push to remote
    print("Pushing to remote...")
    result = subprocess.run(
        ['git', 'push', 'origin', 'main'],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Updates pushed successfully")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"✗ Push failed: {result.stderr}")
        
        # Might need to pull first
        if 'rejected' in result.stderr:
            print()
            print("Pulling first (remote has changes)...")
            subprocess.run(
                ['git', 'pull', '--no-edit', '-X', 'ours'],
                cwd=str(project_root),
                capture_output=True
            )
            
            print("Pushing again...")
            result = subprocess.run(
                ['git', 'push', 'origin', 'main'],
                cwd=str(project_root),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✓ Updates pushed successfully (after pull)")
            else:
                print(f"✗ Push still failed: {result.stderr}")


if __name__ == "__main__":
    main()
