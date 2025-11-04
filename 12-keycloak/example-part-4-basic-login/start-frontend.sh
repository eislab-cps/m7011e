#!/bin/bash

echo "=========================================="
echo "Starting Example Part 4: Basic Login"
echo "=========================================="
echo ""
echo "This example demonstrates:"
echo "  ✓ Keycloak login/logout"
echo "  ✓ Display user information"
echo "  ✓ Show JWT token"
echo ""
echo "No backend needed for this example!"
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
