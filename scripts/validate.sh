#!/bin/bash
# Quick validation script for AI Resume Analyzer

echo "🔍 Running validation checks..."

# Check Python version
python_version=$(python --version 2>&1)
echo "Python version: $python_version"

# Check if all required files exist
required_files=(
    "app.py"
    "requirements.txt" 
    "requirements-dev.txt"
    "backend/resume_analyzer.py"
    "backend/config.py"
    "api/index.py"
    "Dockerfile"
    "docker-compose.yml"
    ".gitignore"
    ".env.example"
)

echo "📁 Checking required files..."
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
    fi
done

# Test imports
echo "🐍 Testing Python imports..."
python -c "
try:
    from backend.resume_analyzer import ResumeAnalyzer
    from backend.config import config
    print('✅ Backend imports successful')
except Exception as e:
    print(f'❌ Import error: {e}')
"

# Check API functionality
echo "🌐 Testing API functionality..."
python -c "
try:
    from api.index import app
    print('✅ FastAPI app can be imported')
except Exception as e:
    print(f'❌ API import error: {e}')
"

# Test basic analysis
echo "🔬 Testing basic analysis..."
python -c "
try:
    from backend.resume_analyzer import ResumeAnalyzer
    analyzer = ResumeAnalyzer()
    test_text = 'John Doe, Software Engineer with Python experience. john@email.com'
    result = analyzer.analyze(test_text)
    assert 'scores' in result
    assert 'technical_skills' in result
    print('✅ Basic analysis working')
except Exception as e:
    print(f'❌ Analysis error: {e}')
"

echo "✨ Validation complete!"