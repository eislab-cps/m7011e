#!/bin/bash

# Script to start the React frontend

echo "================================"
echo "Starting React Frontend"
echo "================================"
echo ""

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
    echo ""
fi

echo "Starting development server..."
echo "Frontend will be available at: http://localhost:3000"
echo ""

npm start
