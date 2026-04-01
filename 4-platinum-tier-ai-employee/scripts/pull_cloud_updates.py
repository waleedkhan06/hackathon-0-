"""
Pull Cloud Updates Script for Platinum Tier AI Employee
Pulls Cloud agent drafts from Git for Local processing
"""
import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    """Pull Cloud updates from Git"""
    print("=" * 60)
    print("Pulling Cloud Updates...")
    print("=" * 60)
    print()
    
    # Check if Git is initialized
    git_dir = project_root / '.git'
    if not git_dir.exists():
        print("✗ Git repository not initialized")
        print("Run: python3 scripts/setup_vault_sync.py")
        sys.exit(1)
    
    # Fetch from remote
    print("Fetching from remote...")
    result = subprocess.run(
        ['git', 'fetch', 'origin'],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"✗ Fetch failed: {result.stderr}")
        sys.exit(1)
    
    print("✓ Fetch successful")
    
    # Pull changes
    print("Pulling updates...")
    result = subprocess.run(
        ['git', 'pull', '--no-edit', '-X', 'ours'],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ Pull successful")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"⚠ Pull had conflicts")
        print("Conflicts resolved using 'ours' strategy (Local changes preserved)")
        
        # Abort merge if conflicts
        subprocess.run(
            ['git', 'merge', '--abort'],
            cwd=str(project_root),
            capture_output=True
        )
    
    # Count Cloud drafts
    updates_dir = project_root / 'updates'
    draft_count = len(list(updates_dir.glob('DRAFT_*.md')))
    
    print()
    print(f"Cloud drafts available: {draft_count}")
    print()
    print("To merge Cloud drafts into Local workflow:")
    print("  python3 scripts/merge_cloud_updates.py")


if __name__ == "__main__":
    main()
