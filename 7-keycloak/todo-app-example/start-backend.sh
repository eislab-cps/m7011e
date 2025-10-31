#!/bin/bash

# Script to start the Flask backend

echo "================================"
echo "Starting Flask Backend"
echo "================================"
echo ""

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Start the server
echo "Starting Flask server..."
echo "Backend will be available at: http://localhost:5000"
echo ""

python app.py
