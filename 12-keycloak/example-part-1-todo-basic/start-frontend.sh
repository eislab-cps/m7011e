#!/bin/bash

echo "=========================================="
echo "Part 4 Example: Todo App WITHOUT Signature Verification"
echo "=========================================="
echo ""
echo "This example demonstrates:"
echo "  ✓ Keycloak login/logout"
echo "  ✓ Full todo CRUD operations"
echo "  ✓ Backend accepts JWT tokens"
echo "  ✗ Backend does NOT verify signatures (insecure!)"
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
