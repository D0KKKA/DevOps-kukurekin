#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INFO_FILE="$PROJECT_DIR/Kukurekin_Danil_info.txt"

echo "=============================="
echo "Student Information"
echo "=============================="
cat "$INFO_FILE"
echo
echo "=============================="
echo "System Information"
echo "=============================="
echo "Username: $(whoami)"
echo "Hostname: $(hostname)"
echo "Current Date: $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "Operating System: $(uname -srm)"
echo "Disk Usage:"
df -h "$PROJECT_DIR" | tail -n 1
echo "Memory Usage:"
if command -v free >/dev/null 2>&1; then
    free -h
else
    vm_stat | head -n 6
fi
echo
if [[ -f "$INFO_FILE" ]]; then
    echo "Student information file exists."
else
    echo "Student information file does not exist."
fi
