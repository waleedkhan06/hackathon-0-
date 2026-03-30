"""
Main script to run the AI Employee Bronze Tier system
"""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from polling_watcher import PollingBasedWatcher
import logging
import time


def main():
    """Start the AI Employee Bronze Tier system"""
    project_path = str(project_root)

    print(f"Starting AI Employee Bronze Tier...")
    print(f"Project path: {project_path}")

    try:
        # Initialize the polling-based file system watcher
        watcher = PollingBasedWatcher(project_path, check_interval=10)

        print("Polling-based watcher initialized. Starting to monitor inbox folder...")
        print("Press Ctrl+C to stop the watcher.")

        # Start watching
        watcher.run()

    except KeyboardInterrupt:
        print("\nShutting down AI Employee Bronze Tier...")
    except Exception as e:
        logging.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    main()