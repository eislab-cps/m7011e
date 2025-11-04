#!/bin/bash

echo "=========================================="
echo "Starting Example Part 5: Backend API"
echo "=========================================="
echo ""
echo "This backend provides:"
echo "  ✓ /api/public    - Public endpoint (no auth)"
echo "  ✓ /api/protected - Protected endpoint (JWT required)"
echo ""
echo "=========================================="
echo ""

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

echo ""
echo "🚀 Starting Flask backend on http://localhost:5001"
echo ""
echo "Endpoints:"
echo "  GET http://localhost:5001/              - Health check"
echo "  GET http://localhost:5001/api/public    - Public (no auth)"
echo "  GET http://localhost:5001/api/protected - Protected (JWT required)"
echo ""
echo "=========================================="
echo ""

python3 app.py
