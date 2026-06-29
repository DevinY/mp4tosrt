#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_ACTIVATE="$SCRIPT_DIR/venv/bin/activate"
if [[ ! -f "$VENV_ACTIVATE" ]]; then
  echo "找不到 venv，請先執行："
  echo "  python3 -m venv venv"
  echo "  source venv/bin/activate"
  echo "  pip install -r requirements.txt"
  exit 1
fi

source "$VENV_ACTIVATE"
python run.py
