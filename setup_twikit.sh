#!/bin/bash

# Twikit Integration Setup Script
# Run this after cloning the repo to set up Twitter integration

echo "============================================================"
echo "🤖 AI Twitter Intern - Twikit Integration Setup"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies (including twikit)..."
pip install -r requirements.txt

# Create data directory
echo "📁 Creating data directory..."
mkdir -p data

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your credentials:"
    echo "   - TWITTER_USERNAME"
    echo "   - TWITTER_EMAIL"
    echo "   - TWITTER_PASSWORD"
    echo "   - GEMINI_API_KEY"
    echo "   - SLACK_WEBHOOK_URL"
    echo ""
else
    echo "✅ .env already exists"
fi

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file with your credentials:"
echo "   nano .env"
echo ""
echo "2. Test Twitter connection:"
echo "   python twitter_client.py"
echo ""
echo "3. Test bot logic (mock data):"
echo "   python test_bot.py"
echo ""
echo "4. Start monitoring (real Twitter):"
echo "   python twitter_monitor.py"
echo ""
echo "📚 Read TWIKIT_INTEGRATION.md for full documentation"
echo ""
