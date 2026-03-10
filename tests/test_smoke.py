import sys
from pathlib import Path

# Ensure project root on sys.path for imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.resume_analyzer import ResumeAnalyzer
from backend.pdf_extractor import extract_text_from_pdf, get_pdf_metadata
from backend.keyword_matcher import calculate_match_score, extract_missing_keywords
import io


def test_analyzer_basic_output():
    """Test basic analyzer functionality."""
    analyzer = ResumeAnalyzer()
    sample_text = "Software engineer with experience in Python, AWS, Docker. Led projects and improved performance by 20%."
    result = analyzer.analyze(sample_text)

    # Verify structure with nested scores
    assert "scores" in result
    assert "technical_skills" in result
    assert "soft_skills" in result
    assert "recommendations" in result
    assert "word_count" in result
    
    # Check scores are in valid range
    assert 0 <= result["scores"]["overall_score"] <= 100
    assert result["scores"]["overall_score"] >= 0


def test_skills_extraction():
    """Test skills extraction functionality."""
    analyzer = ResumeAnalyzer()
    text_with_skills = "Proficient in Python, JavaScript, React, AWS, machine learning, and project management."
    result = analyzer.analyze(text_with_skills)
    
    # Should detect some skills (technical or soft)
    total_skills = len(result["technical_skills"]) + len(result["soft_skills"])
    assert total_skills > 0


def test_empty_text():
    """Test analyzer with empty text."""
    analyzer = ResumeAnalyzer()
    result = analyzer.analyze("")
    
    # Should still return valid structure
    assert isinstance(result, dict)
    assert result["word_count"] == 0


def test_keyword_matcher():
    """Test job matching functionality."""
    resume_text = "Python developer with Django experience and AWS skills"
    job_description = "Looking for Python developer with Django and cloud experience"
    
    score = calculate_match_score(resume_text, job_description)
    
    assert isinstance(score, int)
    assert 0 <= score <= 100
    assert score > 0  # Should have some match


def test_missing_keywords():
    """Test missing keywords extraction."""
    resume_text = "Python developer with experience"
    job_description = "Looking for Python developer with React, AWS, and Docker experience"
    
    missing = extract_missing_keywords(resume_text, job_description)
    
    assert isinstance(missing, list)
    # Should identify React, AWS, Docker as missing
    assert len(missing) > 0


def test_pdf_extractor_error_handling():
    """Test PDF extractor error handling."""
    # Test with invalid data
    invalid_data = io.BytesIO(b"This is not a PDF")
    result = extract_text_from_pdf(invalid_data)
    
    # Should return error message
    assert "Error" in result


def test_score_boundaries():
    """Test that all scores are within valid boundaries."""
    analyzer = ResumeAnalyzer()
    
    # Test with various text lengths
    test_texts = [
        "Short.",
        "This is a medium length resume with some skills like Python and project management experience.",
        "This is a very long resume text that contains many details about experience, education, skills including Python, Java, JavaScript, React, AWS, Docker, machine learning, project management, leadership, communication, teamwork, and many other technical and soft skills that should be detected by the analyzer. It also includes action verbs like developed, managed, led, achieved, implemented, created, designed, improved, analyzed, collaborated, coordinated, and established which should boost the content score."
    ]
    
    for text in test_texts:
        result = analyzer.analyze(text)
        
        # Check all scores are within bounds (now in nested scores dict)
        for key in ["overall_score", "content_quality", "keyword_optimization", "ats_compatibility", "structure_score", "completeness"]:
            score = result["scores"][key]
            assert 0 <= score <= 100, f"{key} score {score} is out of bounds for text length {len(text)}"


def test_recommendations_generation():
    """Test that recommendations are generated."""
    analyzer = ResumeAnalyzer()
    short_text = "Python developer"
    result = analyzer.analyze(short_text)
    
    # Should have recommendations for improvement
    assert len(result["recommendations"]) > 0
    assert all(isinstance(rec, str) for rec in result["recommendations"])
    assert len(result["recommendations"]) <= 6  # Max 6 recommendations