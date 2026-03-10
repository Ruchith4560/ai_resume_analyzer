# Quick validation script for AI Resume Analyzer (Windows PowerShell)

Write-Host "🔍 Running validation checks..." -ForegroundColor Cyan

# Check Python version
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found" -ForegroundColor Red
    exit 1
}

# Check if all required files exist
$requiredFiles = @(
    "app.py",
    "requirements.txt", 
    "requirements-dev.txt",
    "backend/resume_analyzer.py",
    "backend/config.py",
    "api/index.py",
    "Dockerfile",
    "docker-compose.yml",
    ".gitignore",
    ".env.example"
)

Write-Host "📁 Checking required files..." -ForegroundColor Yellow
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file (missing)" -ForegroundColor Red
    }
}

# Test imports
Write-Host "🐍 Testing Python imports..." -ForegroundColor Yellow
$importTest = @"
try:
    from backend.resume_analyzer import ResumeAnalyzer
    from backend.config import config
    print('✅ Backend imports successful')
except Exception as e:
    print(f'❌ Import error: {e}')
"@

python -c $importTest

# Check API functionality
Write-Host "🌐 Testing API functionality..." -ForegroundColor Yellow
$apiTest = @"
try:
    from api.index import app
    print('✅ FastAPI app can be imported')
except Exception as e:
    print(f'❌ API import error: {e}')
"@

python -c $apiTest

# Test basic analysis
Write-Host "🔬 Testing basic analysis..." -ForegroundColor Yellow
$analysisTest = @"
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
"@

python -c $analysisTest

Write-Host "✨ Validation complete!" -ForegroundColor Magenta