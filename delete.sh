#!/bin/bash

# Script directory
PROJECT_ROOT=$(dirname "$BASH_SOURCE")
PROJECT_TMP_DIR="$PROJECT_ROOT/tmp"
mkdir -p "$PROJECT_TMP_DIR"

# Local files
MAIN_PYTHON_SCRIPT="$PROJECT_ROOT/_generate_bash_script.py"
UFW_STATUS_FILE="$PROJECT_TMP_DIR/ufw-status.txt"
DELETE_UFL_RULES_SCRIPT="$PROJECT_TMP_DIR/delete_ufw_rules.sh"

# Save current ufw status to file
echo -n "" >"$UFW_STATUS_FILE"
ufw status >"$UFW_STATUS_FILE" 2>&1

# Generate the script
python3 "$MAIN_PYTHON_SCRIPT" delete

# Run the generated script
# You can comment out this line then manually verify and run the generated script
bash "$DELETE_UFL_RULES_SCRIPT"
