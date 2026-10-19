#!/usr/bin/env bash
# ============================================================
# Steer Metabolic Engine - Unix One-Command Setup (Mac / Linux)
# ============================================================

set -e

echo ""
echo "============================================================"
echo "  Setting up Steer Metabolic Engine..."
echo "============================================================"
echo ""

# 1. Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 not found. Please install Python 3.10 or higher."
    exit 1
fi

# 2. Check virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# 3. Upgrade pip and install requirements
echo "📥 Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run automated setup verification
python setup_pipeline.py

echo ""
echo "🎉 Setup complete! You can now run:"
echo "   source .venv/bin/activate"
echo "   python run_pipeline.py --all"
echo "   python run_pipeline.py --serve"
echo ""
