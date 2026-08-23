#!/bin/zsh
# Regenerate the full diagram set: SVG masters, then 2x PNG exports.
set -e
cd "$(dirname "$0")"
python3 generators/gen_diagrams.py
zsh generators/export.sh
