"""
Test script for Bronze Tier AI Employee functionality
"""
import sys
import os
from pathlib import Path
import time
import json

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_folder_structure():
    """Test that the required folders exist"""
    print("Testing folder structure...")

    required_folders = [
        'inbox',
        'needs_action',
        'done',
        'plans',
        'pending_approval',
        'logs',
        'watchers',
        'mcp_servers',
        'skills'
    ]

    all_good = True
    for folder in required_folders:
        folder_path = project_root / folder
        if folder_path.exists():
            print(f"  ✓ {folder} folder exists")
        else:
            print(f"  ✗ {folder} folder missing")
            all_good = False

    return all_good


def test_files_exist():
    """Test that required files exist"""
    print("\nTesting required files...")

    required_files = [
        'dashboard.md',
        'company_handbook.md',
        'requirements.txt'
    ]

    all_good = True
    for file in required_files:
        file_path = project_root / file
        if file_path.exists():
            print(f"  ✓ {file} exists")
        else:
            print(f"  ✗ {file} missing")
            all_good = False

    return all_good


def test_skills():
    """Test that skill files exist and can be imported"""
    print("\nTesting skills...")

    skill_files = [
        'skills/process_task.py',
        'skills/update_dashboard.py',
        'skills/file_manager.py'
    ]

    all_good = True
    for skill_file in skill_files:
        skill_path = project_root / skill_file
        if skill_path.exists():
            print(f"  ✓ {skill_file} exists")

            # Try to import the skill
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("skill_module", skill_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"  ✓ {skill_file} can be imported")
            except Exception as e:
                print(f"  ✗ {skill_file} import failed: {e}")
                all_good = False
        else:
            print(f"  ✗ {skill_file} missing")
            all_good = False

    return all_good


def test_watcher():
    """Test that watcher files exist"""
    print("\nTesting watchers...")

    watcher_files = [
        'watchers/base_watcher.py',
        'watchers/filesystem_watcher.py'
    ]

    all_good = True
    for watcher_file in watcher_files:
        watcher_path = project_root / watcher_file
        if watcher_path.exists():
            print(f"  ✓ {watcher_file} exists")
        else:
            print(f"  ✗ {watcher_file} missing")
            all_good = False

    return all_good


def test_basic_functionality():
    """Test basic functionality by creating and processing a sample task"""
    print("\nTesting basic functionality...")

    try:
        # Import the skills
        import importlib.util
        file_manager_spec = importlib.util.spec_from_file_location("file_manager", project_root / "skills" / "file_manager.py")
        file_manager_module = importlib.util.module_from_spec(file_manager_spec)
        file_manager_spec.loader.exec_module(file_manager_module)

        process_task_spec = importlib.util.spec_from_file_location("process_task", project_root / "skills" / "process_task.py")
        process_task_module = importlib.util.module_from_spec(process_task_spec)
        process_task_spec.loader.exec_module(process_task_module)

        update_dashboard_spec = importlib.util.spec_from_file_location("update_dashboard", project_root / "skills" / "update_dashboard.py")
        update_dashboard_module = importlib.util.module_from_spec(update_dashboard_spec)
        update_dashboard_spec.loader.exec_module(update_dashboard_module)

        # Test file creation
        print("  Creating a test task file...")
        result = file_manager_module.create_file(
            "needs_action",
            "test_task",
            """---
type: test_task
status: new
priority: medium
---

# Test Task

This is a test task to verify the AI Employee functionality.

## Details
- Created during bronze tier testing
- Should be processed by the system
- Verify all components work together

## Actions Needed
- [ ] Review task
- [ ] Process appropriately
- [ ] Complete or escalate
"""
        )
        if result["status"] == "success":
            print(f"  ✓ Test task created: {result['file_path']}")
            test_task_path = result["file_path"]
        else:
            print(f"  ✗ Failed to create test task: {result['message']}")
            return False

        # List pending tasks
        print("  Listing pending tasks...")
        pending_result = process_task_module.list_pending_tasks()
        if pending_result["status"] == "success":
            print(f"  ✓ Found {pending_result['task_count']} pending tasks")
        else:
            print(f"  ✗ Failed to list pending tasks: {pending_result['message']}")
            return False

        # Process the task
        print("  Processing the test task...")
        process_result = process_task_module.process_task(test_task_path, "complete")
        if process_result["status"] == "success":
            print(f"  ✓ Task processed: {process_result['message']}")
        else:
            print(f"  ✗ Failed to process task: {process_result['message']}")
            return False

        # Update dashboard
        print("  Updating dashboard...")
        dashboard_result = update_dashboard_module.update_dashboard(
            activity="Completed bronze tier functionality test"
        )
        if dashboard_result["status"] == "success":
            print(f"  ✓ Dashboard updated: {dashboard_result['message']}")
        else:
            print(f"  ✗ Failed to update dashboard: {dashboard_result['message']}")
            return False

        print("  ✓ All functionality tests passed!")
        return True

    except Exception as e:
        print(f"  ✗ Error during functionality test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("AI Employee Bronze Tier - Functionality Test")
    print("="*50)

    all_tests_passed = True

    # Run individual tests
    all_tests_passed &= test_folder_structure()
    all_tests_passed &= test_files_exist()
    all_tests_passed &= test_skills()
    all_tests_passed &= test_watcher()
    all_tests_passed &= test_basic_functionality()

    print("\n" + "="*50)
    if all_tests_passed:
        print("✓ ALL TESTS PASSED - Bronze Tier Implementation is Ready!")
        print("\nNext steps for Bronze Tier:")
        print("1. Run 'python main.py' to start the file system watcher")
        print("2. Place files in the 'inbox' folder to trigger processing")
        print("3. Monitor the 'needs_action' folder for tasks to process")
        print("4. Use the skills to manage your AI Employee tasks")
    else:
        print("✗ SOME TESTS FAILED - Please check the errors above")

    return all_tests_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)