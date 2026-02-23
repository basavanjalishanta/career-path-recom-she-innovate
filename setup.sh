#!/bin/bash
# Quick Setup & Run Script for macOS/Linux
# Run this from career_recommendation/v2 directory

set -e

echo "🚀 Career Path - Complete Setup"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python version
echo -e "${BLUE}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi
python_version=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python $python_version${NC}"

# Check Node version
echo -e "${BLUE}Checking Node.js installation...${NC}"
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+"
    exit 1
fi
node_version=$(node --version)
echo -e "${GREEN}✓ Node.js $node_version${NC}"

# Setup Backend
echo ""
echo -e "${BLUE}Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --quiet --upgrade pip setuptools
pip install --quiet -r ../requirements-dev.txt

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Setup Frontend
echo ""
echo -e "${BLUE}Setting up Frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install --silent
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Node modules already installed${NC}"
fi

# Create .env files if they don't exist
cd ../backend
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created backend .env${NC}"
fi

cd ../frontend
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ Created frontend .env${NC}"
fi

cd ..

# Display instructions
echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo -e "${YELLOW}To start the application:${NC}"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm start"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo -e "${BLUE}Happy coding! 🚀${NC}"
