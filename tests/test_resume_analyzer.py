"""
Unit tests for the resume analyzer module.
"""
import sys
from pathlib import Path

# Ensure project root on sys.path for imports
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from backend.resume_analyzer import ResumeAnalyzer


class TestResumeAnalyzer:
    """Test suite for ResumeAnalyzer class."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.analyzer = ResumeAnalyzer()
    
    def test_initialization(self):
        """Test analyzer initialization."""
        assert self.analyzer.technical_skills
        assert self.analyzer.soft_skills
        assert len(self.analyzer.technical_skills) > 30
        assert len(self.analyzer.soft_skills) > 10
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        dirty_text = "  Hello  World!!!  @#$%  "
        clean_text = self.analyzer._clean_text(dirty_text)
        
        # Text should be lowercased and cleaned
        assert "hello" in clean_text
        assert "world" in clean_text
        assert not clean_text.startswith(" ")
        assert not clean_text.endswith(" ")

    def test_analyze_basic_functionality(self):
        """Test basic analyze functionality."""
        text = "I have 5 years of experience with Python, JavaScript, and React. Led team projects and improved performance."
        result = self.analyzer.analyze(text)
        
        # Verify output structure
        assert "overall_score" in result
        assert "technical_skills" in result
        assert "soft_skills" in result
        assert "recommendations" in result
        
        # Verify scores are valid
        assert 0 <= result["overall_score"] <= 100
        assert isinstance(result["technical_skills"], list)
        assert isinstance(result["soft_skills"], list)

    def test_full_analysis(self):
        """Test complete analysis workflow."""
        sample_resume = """
        John Doe
        Software Engineer
        john.doe@email.com
        
        Experience:
        Software Engineer at Tech Company (2020-2023)
        - Developed web applications using Python and JavaScript
        - Led team of 5 developers
        - Improved system performance by 30%
        
        Education:
        Bachelor of Science in Computer Science
        University of Technology (2016-2020)
        
        Skills:
        Python, JavaScript, React, AWS, Docker, Machine Learning
        Leadership, Team Management, Problem Solving
        """
        
        result = self.analyzer.analyze(sample_resume)
        
        # Verify result structure
        assert "overall_score" in result
        assert "technical_skills" in result
        assert "soft_skills" in result
        assert "recommendations" in result
        assert "word_count" in result
        
        # Verify score is valid
        assert 0 <= result["overall_score"] <= 100
        
        # Should detect multiple skills
        total_skills = len(result["technical_skills"]) + len(result["soft_skills"])
        assert total_skills >= 3
        
    def test_empty_text_handling(self):
        """Test handling of empty text."""
        result = self.analyzer.analyze("")
        assert "overall_score" in result
        assert result["overall_score"] >= 0
        
    def test_minimal_text_handling(self):
        """Test handling of minimal text."""
        result = self.analyzer.analyze("Python developer")
        assert "overall_score" in result
        assert isinstance(result["technical_skills"], list)
        assert isinstance(result["recommendations"], list)
        
        # Should have reasonable word count
        assert result["word_count"] > 50
        
        # Should provide recommendations
        assert len(result["recommendations"]) > 0