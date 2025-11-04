#!/bin/bash

echo "=========================================="
echo "Part 4 Example: Backend WITHOUT Signature Verification"
echo "=========================================="
echo ""
echo "⚠️  WARNING: This backend does NOT verify JWT signatures!"
echo "   This is for LEARNING ONLY."
echo "   For secure implementation, see example-part-5"
echo ""
echo "This backend provides:"
echo "  ✓ Full todo CRUD operations"
echo "  ✓ Accepts JWT tokens"
echo "  ✗ Does NOT verify token signatures (INSECURE!)"
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
echo "  GET  http://localhost:5001/api/todos"
echo "  POST http://localhost:5001/api/todos"
echo ""
echo "=========================================="
echo ""

python3 app.py
