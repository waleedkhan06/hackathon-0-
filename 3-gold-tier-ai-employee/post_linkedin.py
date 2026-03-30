#!/usr/bin/env python3
"""
Post to LinkedIn - Simple Command
Auto-detects latest approved LinkedIn post in /approved/

Usage: python3 post_linkedin.py
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent

# Run the LinkedIn poster (it auto-detects the file)
print("\n" + "=" * 70)
print("  📬 LINKEDIN POSTER")
print("=" * 70)
print("\n🔍 Searching for approved LinkedIn posts...")

from skills.linkedin_poster_final import main as linkedin_main

# Call the main function
linkedin_main()
