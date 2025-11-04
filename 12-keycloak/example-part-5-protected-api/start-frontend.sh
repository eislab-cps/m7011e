#!/bin/bash

echo "=========================================="
echo "Starting Example Part 5: Frontend"
echo "=========================================="
echo ""
echo "This example demonstrates:"
echo "  ✓ Everything from Part 4"
echo "  ✓ Call protected Flask API endpoint"
echo "  ✓ Send JWT token in Authorization header"
echo "  ✓ Display API response/errors"
echo ""
echo "⚠️  Make sure backend is running first!"
echo "   Run: ./start-backend.sh in another terminal"
echo ""
echo "=========================================="
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

echo "🚀 Starting React frontend on http://localhost:3000"
echo ""
npm start
