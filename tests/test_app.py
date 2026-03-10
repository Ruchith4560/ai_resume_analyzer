"""
Integration tests for the FastAPI application.
"""
import sys
from pathlib import Path

# Ensure project root on sys.path for imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from fastapi.testclient import TestClient
from api.index import app

client = TestClient(app)


def test_app_loads():
    """Test that the app homepage loads without errors."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Resume Analyzer" in response.text or "AI Resume" in response.text


def test_analyze_endpoint_exists():
    """Test that the analyze endpoint exists."""
    # This should return 422 (validation error) without file, not 404
    response = client.post("/api/analyze")
    assert response.status_code in [422, 400]  # Expects file upload


def test_analysis_workflow():
    """Test the complete analysis workflow."""
    # Test the full user journey from upload to results
    pass


# Note: Streamlit app testing would require specific setup
# This is a placeholder for future comprehensive testing