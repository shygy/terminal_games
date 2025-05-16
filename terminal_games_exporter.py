#!/usr/bin/env python3
"""
Terminal Games Exporter Utility

This utility creates a zip archive of the terminal_games folder with a
versioned filename format: "shygyGames - The Terminal Collection - v.(VERSION_NUMBER).zip"

Usage:
    python terminal_games_exporter.py [version_number] [options]

    If version_number is not provided, the utility will suggest the next version
    from the configuration file or prompt for it.

Options:
    --games-dir PATH    Specify a custom path to the terminal_games directory
    --validate          Validate the ZIP file contents after creation
    --deploy            Copy the ZIP file to the web download folder
    --clean             Clean up old ZIP files
    --keep N            Keep N most recent versions when cleaning (default: 3)
    --history           Show export history and exit

Examples:
    python terminal_games_exporter.py 1.2
    # Creates: "shygyGames - The Terminal Collection - v.1.2.zip"

    python terminal_games_exporter.py 1.3 --games-dir "/path/to/terminal_games"
    # Creates ZIP file using games from the specified directory
"""

import os
import sys
import json
import zipfile
import shutil
import argparse
import tempfile
from datetime import datetime

# Configuration file path (relative to this script)
CONFIG_FILE = "exporter_config.json"

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_version(version):
    """
    Validate that the version number has the correct format.
    
    Args:
        version (str): The version number to validate
        
    Returns:
        bool: True if the version number is valid, False otherwise
    """
    # Simple validation that ensures the version is a number
    # (can be extended with more complex validation if needed)
    try:
        # Try to split by dot to check if it's a valid format like 1.0 or 1.2.3
        parts = version.split('.')
        for part in parts:
            int(part)  # Check if each part is a number
        return True
    except (ValueError, AttributeError):
        return False

def load_config():
    """
    Load the configuration from the JSON file.
    
    Returns:
        dict: The configuration data, or a default configuration if the file doesn't exist
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, CONFIG_FILE)
    
    # Default configuration
    default_config = {
        "last_version": "1.0",
        "next_version": "1.1",
        "export_history": []
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Error reading config file. Using defaults. Error: {e}")
            return default_config
    else:
        print(f"Warning: Config file not found at {config_path}. Using defaults.")
        return default_config

def save_config(config):
    """
    Save the configuration to the JSON file.
    
    Args:
        config (dict): The configuration data to save
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, CONFIG_FILE)
    
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save configuration. Error: {e}")

def update_config_after_export(config, version, zip_path):
    """
    Update the configuration after a successful export.
    
    Args:
        config (dict): The current configuration
        version (str): The version number used for the export
        zip_path (str): The path to the created zip file
        
    Returns:
        dict: The updated configuration
    """
    # Calculate next version (simple increment of the last number)
    parts = version.split('.')
    last_part = int(parts[-1])
    parts[-1] = str(last_part + 1)
    next_version = '.'.join(parts)
    
    # Update configuration
    config["last_version"] = version
    config["next_version"] = next_version
    
    # Add to export history
    export_entry = {
        "version": version,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "filename": os.path.basename(zip_path)
    }
    
    if "export_history" not in config:
        config["export_history"] = []
        
    config["export_history"].append(export_entry)
    
    return config

def create_terminal_games_zip(version, custom_games_dir=None):
    """
    Create a zip archive of the terminal_games folder.
    
    Args:
        version (str): The version number for the zip file name
        custom_games_dir (str, optional): Custom path to the terminal_games directory
        
    Returns:
        tuple: (zip_path, terminal_games_dir) - Path to the created zip file and the directory used
    """
    # Define source and destination paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    # Use custom games directory if provided, otherwise use default path
    if custom_games_dir:
        terminal_games_dir = os.path.abspath(custom_games_dir)
    else:
        terminal_games_dir = os.path.join(repo_root, 'terminal_games')
        
    zip_filename = f"shygyGames - The Terminal Collection - v.{version}.zip"
    zip_path = os.path.join(repo_root, zip_filename)
    
    # Check if terminal_games directory exists
    if not os.path.exists(terminal_games_dir):
        print(f"Error: terminal_games directory not found at {terminal_games_dir}")
        sys.exit(1)
        
    # Delete the zip file if it already exists
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    # Create the ZIP file
    print(f"Creating {zip_filename}...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(terminal_games_dir):
            # Get the relative path from terminal_games_dir
            relpath = os.path.relpath(root, os.path.dirname(terminal_games_dir))
            
            # Skip __pycache__ directories and hidden files/directories
            if '__pycache__' in root or '/.' in root:
                continue
                
            # Create directory entries in the zip file
            if relpath != '.':
                zipf.write(root, relpath)
                
            # Add files to the zip
            for file in files:
                # Skip hidden files, __pycache__, and compiled Python files
                if file.startswith('.') or file.endswith('.pyc'):
                    continue
                    
                filepath = os.path.join(root, file)
                # Add file to zip with appropriate internal path
                zipf.write(filepath, os.path.join(relpath, file))
    
    print(f"Successfully created: {zip_path}")
    return zip_path, terminal_games_dir

def validate_zip(zip_path):
    """
    Validate the contents of a ZIP file.
    
    Args:
        zip_path (str): Path to the ZIP file to validate
        
    Returns:
        bool: True if validation passed, False otherwise
    """
    print(f"\nValidating {os.path.basename(zip_path)}...")
    
    try:
        # Check if the file exists and is a valid ZIP
        if not os.path.exists(zip_path):
            print(f"Error: ZIP file not found at {zip_path}")
            return False
            
        if not zipfile.is_zipfile(zip_path):
            print(f"Error: {zip_path} is not a valid ZIP file")
            return False
            
        # Try to open and read the ZIP file
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            # Check for file integrity
            test_result = zipf.testzip()
            if test_result:
                print(f"Error: ZIP file has corrupt file: {test_result}")
                return False
                
            # List files to verify structure
            file_list = zipf.namelist()
            if not file_list:
                print("Error: ZIP file is empty")
                return False
                
            # Check for expected structure (at least one Python file in terminal_games/)
            python_files = [f for f in file_list if f.endswith('.py')]
            if not python_files:
                print("Error: No Python files found in ZIP")
                return False
                
            # Check for main game files
            essential_files = [
                'terminal_games/blackJack.py',
                'terminal_games/highOrLow.py',
                'terminal_games/rpsBasic.py',
                'terminal_games/hangman.py',
                'terminal_games/game_selector.py'
            ]
            
            missing_files = [f for f in essential_files if f not in file_list]
            if missing_files:
                print("Warning: Some essential files are missing:")
                for f in missing_files:
                    print(f"  - {f}")
                    
            # Check for startup scripts
            if 'terminal_games/start_games.bat' not in file_list:
                print("Warning: Windows startup script (start_games.bat) is missing")
            if 'terminal_games/start_games.sh' not in file_list:
                print("Warning: Unix startup script (start_games.sh) is missing")
                
            # Extract a sample file to verify content
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract a Python file to check
                sample_file = python_files[0]
                zipf.extract(sample_file, temp_dir)
                extracted_path = os.path.join(temp_dir, sample_file)
                
                # Check if the file has content
                if os.path.getsize(extracted_path) == 0:
                    print(f"Warning: Extracted file {sample_file} is empty")
                    
        print("Validation complete: ZIP file appears to be valid")
        return True
        
    except Exception as e:
        print(f"Error during validation: {e}")
        return False

def clean_old_zip_files(config, keep_count=3):
    """
    Clean up old ZIP files, keeping only the most recent ones.
    
    Args:
        config (dict): The configuration containing the export history
        keep_count (int): Number of most recent ZIP files to keep
        
    Returns:
        int: Number of files deleted
    """
    if "export_history" not in config or not config["export_history"]:
        print("No export history found.")
        return 0
        
    # Sort export history by version (assuming version numbers are comparable)
    # This assumes newer versions have higher version numbers
    try:
        sorted_history = sorted(
            config["export_history"], 
            key=lambda x: [int(p) for p in x["version"].split('.')],
            reverse=True
        )
    except (ValueError, KeyError):
        # Fall back to sorting by date if version sorting fails
        sorted_history = sorted(
            config["export_history"],
            key=lambda x: x.get("date", ""),
            reverse=True
        )
    
    # Keep the most recent ones
    to_keep = sorted_history[:keep_count]
    to_delete = sorted_history[keep_count:]
    
    if not to_delete:
        print(f"No files to clean up. Keeping all {len(to_keep)} ZIP files.")
        return 0
    
    # Get the filenames to keep for display
    keep_filenames = [entry["filename"] for entry in to_keep]
    print(f"Keeping {len(keep_filenames)} most recent ZIP files:")
    for filename in keep_filenames:
        print(f"  - {filename}")
    
    # Delete the older files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    deleted_count = 0
    print(f"\nDeleting {len(to_delete)} older ZIP files:")
    for entry in to_delete:
        filename = entry["filename"]
        filepath = os.path.join(repo_root, filename)
        
        print(f"  - {filename} (version {entry['version']}, {entry['date']})")
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                deleted_count += 1
            except OSError as e:
                print(f"    Error deleting {filename}: {e}")
        else:
            print(f"    File not found: {filename}")
    
    # Update the export history in the config
    if deleted_count > 0:
        config["export_history"] = to_keep
        print(f"\nRemoved {deleted_count} old ZIP files and updated export history.")
    
    return deleted_count

def deploy_to_web_folder(zip_path, config):
    """
    Copy the ZIP file to the web download folder.
    
    This makes the terminal games package available for download
    through the web application.
    
    Args:
        zip_path (str): Path to the ZIP file to deploy
        config (dict): The configuration containing deploy settings
        
    Returns:
        bool: True if the deployment was successful, False otherwise
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    # Define the web download folder (adjust as needed)
    web_download_folder = os.path.join(repo_root, "static", "downloads")
    
    # Ensure the download folder exists
    if not os.path.exists(web_download_folder):
        try:
            os.makedirs(web_download_folder)
            print(f"Created download directory: {web_download_folder}")
        except OSError as e:
            print(f"Error creating download directory: {e}")
            return False
    
    # Copy the ZIP file to the download folder
    zip_filename = os.path.basename(zip_path)
    web_zip_path = os.path.join(web_download_folder, zip_filename)
    
    try:
        shutil.copy2(zip_path, web_zip_path)
        print(f"Successfully deployed ZIP file to web download folder:")
        print(f"  - Source: {zip_path}")
        print(f"  - Destination: {web_zip_path}")
        
        # Also copy to a "latest" file that always points to the most recent version
        latest_zip_path = os.path.join(web_download_folder, "shygyGames - The Terminal Collection - Latest.zip")
        shutil.copy2(zip_path, latest_zip_path)
        print(f"  - Also copied to: {latest_zip_path}")
        
        # Save the latest version info for the web application
        version_info_path = os.path.join(web_download_folder, "version_info.json")
        version_info = {
            "latest_version": os.path.basename(zip_path).split("v.")[-1].split(".zip")[0],
            "file_size_kb": round(os.path.getsize(zip_path) / 1024, 1),
            "updated_date": datetime.now().strftime("%Y-%m-%d"),
            "filename": zip_filename
        }
        
        with open(version_info_path, 'w') as f:
            json.dump(version_info, f, indent=2)
            
        print(f"  - Created version info file: {version_info_path}")
        return True
        
    except (IOError, OSError) as e:
        print(f"Error deploying ZIP file: {e}")
        return False

def update_changelog(terminal_games_dir, version, description=None):
    """
    Update the changelog.txt file with a new version entry.
    
    Args:
        terminal_games_dir (str): Path to the terminal_games directory
        version (str): The version number to add to changelog
        description (str, optional): A short description of the changes
        
    Returns:
        bool: True if changelog was updated, False otherwise
    """
    # Get the current date
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    
    # Set default description if none is provided
    if not description:
        description = "Maintenance update"
    
    # Format for the new changelog entry
    new_entry = (
        f"shygyGames - The Terminal Collection v.{version} - {today}\n"
        f"----------------------------------------------------------------------------\n"
        f"{description}\n"
        "==========================================\n"
    )
    
    changelog_path = os.path.join(terminal_games_dir, "changelog.txt")
    
    try:
        if os.path.exists(changelog_path):
            # Read existing changelog
            with open(changelog_path, 'r') as f:
                existing_content = f.read()
            
            # Write new entry on top of existing content
            with open(changelog_path, 'w') as f:
                f.write(new_entry + existing_content)
        else:
            # Create new changelog file
            with open(changelog_path, 'w') as f:
                f.write(new_entry)
                f.write(f"shygyGames - The Terminal Collection v.1.0 - {today}\n")
                f.write("----------------------------------------------------------------------------\n")
                f.write("Initial release\n")
                f.write("- Initial collection of terminal games\n")
        
        print(f"Updated changelog.txt with version {version}")
        return True
    except Exception as e:
        print(f"Warning: Could not update changelog.txt: {e}")
        return False

def show_export_history(config):
    """
    Display the export history from the configuration.
    
    Args:
        config (dict): The configuration containing the export history
    """
    if "export_history" not in config or not config["export_history"]:
        print("No export history found.")
        return
        
    print("\nExport History:")
    print("-" * 60)
    print(f"{'Version':<10} {'Date':<12} {'Filename'}")
    print("-" * 60)
    
    for entry in config["export_history"]:
        print(f"{entry['version']:<10} {entry['date']:<12} {entry['filename']}")

def main():
    """
    Main function to run the terminal games exporter utility.
    
    This function handles command line arguments, validates user input,
    and calls the function to create the zip archive.
    
    Returns:
        None
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Create a zip archive of the terminal_games folder.'
    )
    parser.add_argument(
        'version', nargs='?', default=None,
        help='Version number for the zip file (e.g., 1.0 or 1.2.3)'
    )
    parser.add_argument(
        '--history', action='store_true',
        help='Show export history and exit'
    )
    parser.add_argument(
        '--validate', action='store_true',
        help='Validate the created ZIP file after export'
    )
    parser.add_argument(
        '--clean', action='store_true',
        help='Clean up old ZIP files, keeping only the most recent ones'
    )
    parser.add_argument(
        '--keep', type=int, default=3,
        help='Number of most recent ZIP files to keep when cleaning (default: 3)'
    )
    parser.add_argument(
        '--deploy', action='store_true',
        help='Copy the created ZIP file to the web download folder'
    )
    parser.add_argument(
        '--games-dir', type=str, default=None,
        help='Custom path to the terminal_games directory (if different from default)'
    )
    parser.add_argument(
        '--description', type=str, default=None,
        help='Short description of changes for the changelog'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    # Clear screen and show title
    clear_screen()
    print("=" * 60)
    print(" " * 10 + "TERMINAL GAMES EXPORTER UTILITY")
    print("=" * 60)
    print()
    
    # Show history if requested
    if args.history:
        show_export_history(config)
        sys.exit(0)
        
    # Clean up old ZIP files if requested
    if args.clean:
        deleted_count = clean_old_zip_files(config, args.keep)
        save_config(config)
        if not args.version:  # If only cleaning, exit
            sys.exit(0)
    
    # Get version number from arguments, config suggestion, or prompt
    version = args.version
    
    if not version:
        # Suggest next version from config
        suggested_version = config.get("next_version", "1.0")
        print(f"Suggested version: {suggested_version} (from config)")
        version = input(f"Enter version number (press Enter for {suggested_version}): ")
        
        if not version:
            version = suggested_version
    
    # Validate version
    while not validate_version(version):
        print(f"Invalid version format: {version}")
        print("Please use a numeric format like 1.0 or 1.2.3")
        version = input("Enter version number: ")
        if not version:
            print("Version number cannot be empty.")
    
    # Get the games directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    # Use custom games directory if provided, otherwise use default path
    terminal_games_dir = os.path.join(repo_root, 'terminal_games')
    if args.games_dir:
        terminal_games_dir = os.path.abspath(args.games_dir)
    
    # Update the changelog with the new version if description is provided
    if args.description:
        update_changelog(terminal_games_dir, version, args.description)
    
    # Create the zip file
    zip_path, games_dir_used = create_terminal_games_zip(version, args.games_dir)
    
    # Validate the zip file if requested
    if args.validate:
        validation_result = validate_zip(zip_path)
        if not validation_result:
            print("\nWarning: ZIP file validation failed.")
            if input("Continue anyway? (y/n): ").lower() != 'y':
                print("Export aborted. ZIP file remains but configuration was not updated.")
                sys.exit(1)
    
    # Update and save configuration
    updated_config = update_config_after_export(config, version, zip_path)
    save_config(updated_config)
    
    # Deploy to web folder if requested
    if args.deploy:
        deploy_success = deploy_to_web_folder(zip_path, config)
        if not deploy_success:
            print("Warning: Failed to deploy ZIP file to web download folder.")
    
    print("\nExport complete!")
    print(f"Zip file created: {os.path.basename(zip_path)}")
    print(f"Location: {os.path.abspath(zip_path)}")
    print(f"Games directory used: {games_dir_used}")
    print(f"Next suggested version: {updated_config['next_version']}")
    print(f"File size: {os.path.getsize(zip_path) / 1024:.1f} KB")
    print("\nYou can distribute this file for users to download and play the terminal games offline.")
    print("\nUseful flags:")
    print("  --history   : Show export history")
    print("  --validate  : Verify ZIP file contents after creation")
    print("  --clean     : Clean up old ZIP files, keeping only recent ones")
    print("  --keep N    : Keep N most recent versions when cleaning (default: 3)")
    print("  --deploy    : Copy the ZIP file to the web download folder")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExport canceled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)