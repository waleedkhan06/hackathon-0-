"""
Merge Cloud Updates Script for Platinum Tier AI Employee
Merges Cloud agent drafts from /Updates/ to /Needs_Action/
"""
import os
import sys
import shutil
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    """Merge Cloud updates into Local workflow"""
    print("=" * 60)
    print("Merging Cloud Updates...")
    print("=" * 60)
    print()
    
    updates_dir = project_root / 'updates'
    needs_action_dir = project_root / 'needs_action'
    signals_dir = project_root / 'signals'
    logs_archive = project_root / 'logs' / 'signals_archive'
    
    # Ensure directories exist
    needs_action_dir.mkdir(parents=True, exist_ok=True)
    logs_archive.mkdir(parents=True, exist_ok=True)
    
    # Merge Cloud drafts
    merged_count = 0
    
    print("Checking for Cloud drafts...")
    for draft_file in updates_dir.glob('DRAFT_*.md'):
        dest = needs_action_dir / draft_file.name
        
        if not dest.exists():
            shutil.move(str(draft_file), str(dest))
            merged_count += 1
            print(f"  ✓ Merged: {draft_file.name}")
        else:
            print(f"  ⊘ Skipped (already exists): {draft_file.name}")
    
    print()
    print(f"Merged {merged_count} Cloud drafts")
    
    # Process signals
    signal_count = 0
    print()
    print("Processing signals...")
    
    for signal_file in signals_dir.glob('*.json'):
        try:
            import json
            signal_content = json.loads(signal_file.read_text())
            
            signal_type = signal_content.get('type', 'unknown')
            created_by = signal_content.get('created_by', 'unknown')
            
            print(f"  Signal from {created_by}: {signal_type}")
            
            # Archive signal
            archive_path = logs_archive / signal_file.name
            shutil.move(str(signal_file), str(archive_path))
            signal_count += 1
            
        except Exception as e:
            print(f"  ✗ Error processing signal: {signal_file.name}")
    
    print()
    print(f"Processed {signal_count} signals")
    
    print()
    print("=" * 60)
    print("Merge Complete!")
    print("=" * 60)
    print()
    print(f"Cloud drafts merged: {merged_count}")
    print(f"Signals processed: {signal_count}")
    print()
    print("Cloud drafts are now in /needs_action/")
    print("Start Local Agent to process:")
    print("  python3 main.py")


if __name__ == "__main__":
    main()
