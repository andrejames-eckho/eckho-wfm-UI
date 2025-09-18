#!/bin/bash

# Eckho WFM Database Startup Script
echo "🚀 Starting Eckho WFM Database Setup..."

# Start PostgreSQL with Docker Compose
echo "📦 Starting PostgreSQL container..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 10

# Check if PostgreSQL is running
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Failed to start PostgreSQL container"
    exit 1
fi

echo "✅ PostgreSQL container is running"

# Install Python dependencies if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Installing Python dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Initialize database with dummy data
    echo "🗄️ Initializing database with dummy employee data..."
    python init_db.py
    
    echo "🎉 Database setup complete!"
    echo ""
    echo "📋 Database Information:"
    echo "  - Host: localhost"
    echo "  - Port: 5432"
    echo "  - Database: eckho_wfm"
    echo "  - Username: eckho_user"
    echo "  - Password: eckho_password"
    echo ""
    echo "👥 Test Accounts:"
    echo "  Admin: admin / admin123"
    echo "  Employee: john.smith / emp123"
    echo "  Employee: sarah.johnson / emp123"
    echo "  (and 9 more employees with password: emp123)"
    echo ""
    echo "🚀 To start the backend server:"
    echo "  python main.py"
else
    echo "⚠️  Virtual environment not found. Please create one and install dependencies:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo "  python init_db.py"
fi
