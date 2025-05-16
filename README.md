# Terminal Games Exporter Utility

A Python utility for creating versioned ZIP archives of the terminal games collection.

## Overview

This utility helps manage the creation and distribution of the "shygyGames - The Terminal Collection" package by:

1. Creating properly formatted ZIP archives of the terminal games
2. Managing version numbers and export history
3. Maintaining a changelog of version updates
4. Deploying packages to the web download folder
5. Validating package contents
6. Cleaning up old versions

## Usage

Run the utility from the utils directory:

```bash
python terminal_games_exporter.py [version] [options]
```

If no version is provided, the utility will suggest the next version from the configuration or prompt for one.

### Basic Examples

Create a new version:
```bash
python terminal_games_exporter.py 1.5
```

Create a version with changelog entry:
```bash
python terminal_games_exporter.py 1.5 --description "New features and bug fixes"
```

Validate a created ZIP file:
```bash
python terminal_games_exporter.py 1.5 --validate
```

Deploy to web download folder:
```bash
python terminal_games_exporter.py 1.5 --deploy
```

View export history:
```bash
python terminal_games_exporter.py --history
```

Clean up old ZIP files:
```bash
python terminal_games_exporter.py --clean --keep 3
```

## Command-Line Options

| Option | Description |
|--------|-------------|
| `version` | The version number for the ZIP file (e.g., 1.0 or 1.2.3) |
| `--history` | Show export history and exit |
| `--validate` | Validate the created ZIP file after export |
| `--clean` | Clean up old ZIP files, keeping only the most recent ones |
| `--keep N` | Number of most recent ZIP files to keep when cleaning (default: 3) |
| `--deploy` | Copy the created ZIP file to the web download folder |
| `--games-dir PATH` | Custom path to the terminal_games directory (if different from default) |
| `--description TEXT` | Short description of changes for the changelog |

## Features

### Version Management

The utility tracks version numbers and suggests the next logical version based on previous exports. Versions should follow a numeric format like "1.0" or "1.2.3".

### Changelog Generation

When using the `--description` parameter, the utility will update the changelog.txt file in the terminal_games directory with the new version entry. The changelog follows this format:

```
shygyGames - The Terminal Collection v.(version number) - date (not time)
----------------------------------------------------------------------------
<description>
==========================================
<previous changes>
```

### Export History

The utility keeps track of all previous exports in the configuration file. You can view this history using the `--history` flag.

### ZIP File Validation

The `--validate` option checks the contents of the created ZIP file to ensure it contains all necessary files and has the correct structure.

### Web Deployment

The `--deploy` option copies the ZIP file to the web download folder (static/downloads) and creates:
- A versioned ZIP file (e.g., "shygyGames - The Terminal Collection - v.1.5.zip")
- A "Latest" file for easy access (shygyGames - The Terminal Collection - Latest.zip)
- A version_info.json file with metadata about the latest version

### Custom Terminal Games Path

The `--games-dir` option allows exporting from a custom location when using the utility on a different computer or from a non-standard directory structure.

### File Cleanup

The `--clean` option removes old ZIP files while keeping a specified number of recent versions (default: 3).

## Configuration

The utility stores its configuration in `exporter_config.json` in the same directory as the script. This file contains:

- The next suggested version number
- Export history (date, version, filename)
- Web deployment settings

## File Structure

The exported ZIP file follows this structure:

```
terminal_games/
├── launch_games.py - Main launcher script
├── shygyGames - README.md - Documentation file
├── start_games.bat - Windows launcher script
├── start_games.sh - Unix launcher script
├── changelog.txt - Version history
├── game_selector.py - Game selection menu
├── blackJack.py - Blackjack game
├── hangman.py - Hangman game
├── wordlist.py - Word list for Hangman
├── highOrLow.py - Number guessing game
└── rpsBasic.py - Rock Paper Scissors game
```

## Tips for Use

1. Always use the `--validate` flag to ensure the ZIP file is properly created
2. Include a meaningful description with the `--description` flag to maintain an informative changelog
3. Use the `--deploy` flag to make the ZIP file available for web download
4. Periodically run with the `--clean` flag to remove old versions and save disk space
5. When exporting on a different computer, use the `--games-dir` flag to specify the location of the terminal_games folder