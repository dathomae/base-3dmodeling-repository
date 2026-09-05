#!/usr/bin/env bash
set -euo pipefail

# Change to the repository root (where this script lives).
cd "$(dirname "$0")"

if [[ -d .venv ]]; then
    echo "Removing existing .venv for a clean setup ..."
    rm -rf .venv
fi

echo "Creating Python virtual environment in .venv ..."
python3 -m venv .venv

echo "Upgrading pip ..."
.venv/bin/python -m pip install --upgrade pip -q

echo "Installing package in editable mode (build123d + pytest) ..."
.venv/bin/python -m pip install -e . -q

cat <<'EOF'

Setup complete.

Next steps:
  .venv/bin/python -m pytest              # run the test suite
  .venv/bin/python -m scaffold.example    # generate manufacture/scaffold_box.step

Model-viewer hint: install and use ocp_vscode in VS Code to view generated .step files.
EOF
