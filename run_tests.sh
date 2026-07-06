#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "🚀 Starting CI Test Automation Pipeline..."
echo "========================================="

if [ -f "env/Scripts/activate" ]; then
    echo "✔ Windows Virtual Environment detected. Activating..."
    # shellcheck disable=SC1091
    source env/Scripts/activate
elif [ -f "env/bin/activate" ]; then
    echo "✔ Linux/CI Virtual Environment detected. Activating..."
    # shellcheck disable=SC1091
    source env/bin/activate
else
    echo "❌ CRITICAL ERROR: Python virtual environment folder 'env' not found!"
    exit 1
fi

echo "⚡ Running your 15 programmatic tests via PyTest..."
if python -m pytest test_app.py -vv; then
    echo "====================================================="
    echo "🎉 SUCCESS: All 15 tests passed! Safe to merge code."
    echo "====================================================="
    exit 0
else
    echo "====================================================="
    echo "💥 FAILURE: Test suite failed! Blocking deployment pipeline."
    echo "====================================================="
    exit 1
fi


