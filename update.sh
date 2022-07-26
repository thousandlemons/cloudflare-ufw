#!/bin/bash

# Script directory
PROJECT_ROOT=$(dirname "$BASH_SOURCE")
PROJECT_TMP_DIR="$PROJECT_ROOT/tmp"
mkdir -p "$PROJECT_TMP_DIR"

# Local files
MAIN_PYTHON_SCRIPT="$PROJECT_ROOT/_generate_bash_script.py"
UFW_STATUS_FILE="$PROJECT_TMP_DIR/ufw-status.txt"
CLOUDFLARE_IPS_FILE="$PROJECT_TMP_DIR/cloudflare-ips.txt"
UPDATE_UFW_RULES_SCRIPT="$PROJECT_TMP_DIR/update_ufw_rules.sh"

# Cloudflare IP URLs
CLOUDFLARE_IPV4_URL="https://www.cloudflare.com/ips-v4"
CLOUDFLARE_IPV6_URL="https://www.cloudflare.com/ips-v6"

# Save current ufw status to file
echo -n "" >"$UFW_STATUS_FILE"
ufw status >"$UFW_STATUS_FILE" 2>&1

# Fetch latest Cloudflare IPs and save to file
curl -s "$CLOUDFLARE_IPV4_URL" >"$CLOUDFLARE_IPS_FILE"
echo "" >>"$CLOUDFLARE_IPS_FILE"
curl -s "$CLOUDFLARE_IPV6_URL" >>"$CLOUDFLARE_IPS_FILE"
echo "" >>"$CLOUDFLARE_IPS_FILE"

# Generate the script
python3 "$MAIN_PYTHON_SCRIPT" update

# Run the generated script
# You can comment out this line then manually verify and run the generated script
bash "$UPDATE_UFW_RULES_SCRIPT"
