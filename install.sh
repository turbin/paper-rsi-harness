#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
  echo 'Usage: bash install.sh "/path/to/paper-rsi-harness"' >&2
  exit 2
fi
command -v python3 >/dev/null || { echo 'Install Python 3.10+ first.' >&2; exit 1; }
command -v git >/dev/null || { echo 'Install Git first.' >&2; exit 1; }
python3 -c 'import sys; assert sys.version_info >= (3,10), "Python 3.10+ required"'
paper_script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$paper_script_dir/paper.py" init --root "$1"
