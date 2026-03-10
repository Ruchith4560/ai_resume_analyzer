#!/bin/bash
# Vercel Build Optimization Script
# This script optimizes the deployment package for Vercel's 250MB limit

set -e

echo "🚀 Starting Vercel build optimization..."

# Step 1: Clean up Python cache
echo "📦 Cleaning Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Step 2: Remove unnecessary directories
echo "🧹 Removing unnecessary directories..."
rm -rf tests/ .git/ .github/ docs/ scripts/ .vscode/ .idea/ 2>/dev/null || true
rm -f app.py check_deployment.py verify_project.py test_local.py 2>/dev/null || true
rm -f *.md 2>/dev/null || true

# Step 3: Verify final size
echo "📊 Checking package size..."
TOTAL_SIZE=$(du -sh . | cut -f1)
echo "✅ Final package size: $TOTAL_SIZE"

# Step 4: Download minimal NLTK data
echo "📥 Downloading minimal NLTK data..."
python3 -c "
import nltk
import os

# Download only required data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Show what was downloaded
print('✅ NLTK data downloaded')
"

echo "✅ Build optimization complete!"