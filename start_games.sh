#!/bin/bash
# Script to start the terminal games

# Find the Python executable
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "Error: Python is not installed or not in your PATH"
    echo "Please install Python 3 to run these games"
    exit 1
fi

# Navigate to the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Run the launcher script
$PYTHON launch_games.py