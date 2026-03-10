"""
Enhanced test suite for Resume Analyzer with comprehensive coverage
"""
import sys
import pytest
from pathlib import Path
import logging

# Add project root to path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.resume_analyzer import ResumeAnalyzer
from backend.keyword_matcher import calculate_match_score, extract_missing_keywords, get_keyword_suggestions
from backend.pdf_extractor import extract_text_from_pdf, extract_text_from_docx

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)

class TestResumeAnalyzer:
    """Comprehensive test suite for ResumeAnalyzer class."""
    
    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup for each test method."""
        self.analyzer = ResumeAnalyzer()
    
    def test_initialization(self):
        """Test analyzer initialization."""
        assert self.analyzer.technical_skills
        assert self.analyzer.soft_skills
        assert self.analyzer.action_verbs
        assert len(self.analyzer.technical_skills) > 30
        assert len(self.analyzer.soft_skills) > 8
        assert len(self.analyzer.action_verbs) > 15

    def test_analyze_with_valid_resume(self, sample_resume_text):
        """Test analyze method with valid resume."""
        result = self.analyzer.analyze(sample_resume_text)
        
        # Check result structure
        required_keys = [
            'scores', 'technical_skills', 'soft_skills', 'action_verbs',
            'word_count', 'sections_detected', 'contact_info', 'recommendations'
        ]
        for key in required_keys:
            assert key in result
        
        # Check scores structure
        score_keys = [
            'overall_score', 'content_quality', 'keyword_optimization',
            'ats_compatibility', 'structure_score', 'completeness'
        ]
        scores = result['scores']
        for key in score_keys:
            assert key in scores
            assert 0 <= scores[key] <= 100
        
        # Check that skills were detected
        assert len(result['technical_skills']) > 0
        assert len(result['soft_skills']) > 0
        assert result['word_count'] > 100

    def test_analyze_with_minimal_resume(self, minimal_resume_text):
        """Test analyze with minimal resume."""
        result = self.analyzer.analyze(minimal_resume_text)
        
        assert result['scores']['overall_score'] >= 0
        assert result['word_count'] > 0
        assert len(result['recommendations']) > 0

    def test_analyze_with_empty_text(self, empty_resume_text):
        """Test analyze with empty text."""
        result = self.analyzer.analyze(empty_resume_text)
        
        assert result['scores']['overall_score'] == 0
        assert result['word_count'] == 0
        assert len(result['technical_skills']) == 0

    def test_analyze_with_invalid_input(self):
        """Test analyze with invalid input types."""
        with pytest.raises(ValueError):
            self.analyzer.analyze(None)
        
        with pytest.raises(ValueError):
            self.analyzer.analyze(123)
        
        with pytest.raises(ValueError):
            self.analyzer.analyze(['not', 'a', 'string'])

    def test_skill_extraction(self, sample_resume_text):
        """Test skill extraction functionality."""
        result = self.analyzer.analyze(sample_resume_text)
        
        # Should detect Python, JavaScript, React from sample text
        tech_skills = [skill.lower() for skill in result['technical_skills']]
        assert 'python' in tech_skills
        assert 'javascript' in tech_skills
        
        # Should detect leadership from sample text
        soft_skills = [skill.lower() for skill in result['soft_skills']]
        assert any('leadership' in skill.lower() for skill in result['soft_skills'])

    def test_action_verbs_detection(self, sample_resume_text):
        """Test action verbs detection."""
        result = self.analyzer.analyze(sample_resume_text)
        
        action_verbs = [verb.lower() for verb in result['action_verbs']]
        # Sample text should contain 'developed', 'led', 'improved'
        assert 'developed' in action_verbs
        assert 'led' in action_verbs
        assert result['action_verbs_count'] > 0

    def test_sections_detection(self, sample_resume_text):
        """Test section detection functionality."""
        result = self.analyzer.analyze(sample_resume_text)
        
        sections = result['sections_detected']
        assert 'Experience' in sections
        assert 'Education' in sections
        assert 'Skills' in sections

    def test_contact_info_extraction(self, sample_resume_text):
        """Test contact information extraction."""
        result = self.analyzer.analyze(sample_resume_text)
        
        contact_info = result['contact_info']
        assert contact_info['has_email'] == True
        assert contact_info['has_phone'] == True
        assert contact_info['has_linkedin'] == True

    def test_scoring_logic(self):
        """Test scoring calculation logic."""
        # Test with good resume
        good_resume = """
        John Doe, Software Engineer
        john@email.com | (555) 123-4567
        
        EXPERIENCE
        Senior Developer (2020-2023)
        • Developed 5 applications using Python and React
        • Led team of 8 developers, increasing productivity by 40%
        • Implemented CI/CD reducing deployment time by 60%
        
        EDUCATION
        BS Computer Science, MIT (2020)
        
        SKILLS
        Python, JavaScript, React, AWS, Docker, Leadership, Communication
        """
        
        result = self.analyzer.analyze(good_resume)
        scores = result['scores']
        
        # Good resume should score reasonably well
        assert scores['overall_score'] > 50
        assert scores['content_quality'] > 40
        assert scores['keyword_optimization'] > 30
        assert scores['ats_compatibility'] > 60

    def test_recommendations_generation(self, minimal_resume_text):
        """Test that recommendations are generated appropriately."""
        result = self.analyzer.analyze(minimal_resume_text)
        
        recommendations = result['recommendations']
        assert len(recommendations) > 0
        assert len(recommendations) <= 6  # Max recommendations
        
        # Should contain actionable advice
        rec_text = ' '.join(recommendations).lower()
        assert any(word in rec_text for word in ['add', 'include', 'improve', 'use'])


class TestKeywordMatcher:
    """Test suite for keyword matching functionality."""
    
    def test_calculate_match_score_basic(self, sample_resume_text, job_description_text):
        """Test basic match score calculation."""
        score = calculate_match_score(sample_resume_text, job_description_text)
        
        assert isinstance(score, int)
        assert 0 <= score <= 100
        assert score > 0  # Should find some matches

    def test_calculate_match_score_empty_inputs(self):
        """Test match score with empty inputs."""
        assert calculate_match_score("", "job description") == 0
        assert calculate_match_score("resume text", "") == 0
        assert calculate_match_score("", "") == 0

    def test_calculate_match_score_invalid_inputs(self):
        """Test match score with invalid inputs."""
        with pytest.raises(ValueError):
            calculate_match_score(None, "job description")
        
        with pytest.raises(ValueError):
            calculate_match_score("resume text", None)

    def test_extract_missing_keywords(self, sample_resume_text, job_description_text):
        """Test missing keywords extraction."""
        missing = extract_missing_keywords(sample_resume_text, job_description_text)
        
        assert isinstance(missing, list)
        assert len(missing) <= 10  # Max 10 keywords
        
        # All items should be strings
        assert all(isinstance(keyword, str) for keyword in missing)

    def test_extract_missing_keywords_invalid_inputs(self):
        """Test missing keywords with invalid inputs."""
        with pytest.raises(ValueError):
            extract_missing_keywords(None, "job description")

    def test_get_keyword_suggestions(self, job_description_text):
        """Test keyword suggestions generation."""
        suggestions = get_keyword_suggestions(job_description_text)
        
        assert isinstance(suggestions, dict)
        required_keys = ['technical_skills', 'soft_skills', 'action_verbs']
        for key in required_keys:
            assert key in suggestions
            assert isinstance(suggestions[key], list)

    def test_get_keyword_suggestions_invalid_input(self):
        """Test keyword suggestions with invalid input."""
        with pytest.raises(ValueError):
            get_keyword_suggestions(None)
        
        # Empty string should return empty suggestions
        result = get_keyword_suggestions("")
        assert all(len(suggestions) == 0 for suggestions in result.values())


class TestPDFExtractor:
    """Test suite for PDF and document extraction."""
    
    def test_extract_text_from_pdf_invalid_input(self):
        """Test PDF extraction with invalid input."""
        with pytest.raises(ValueError):
            extract_text_from_pdf(None)
        
        with pytest.raises(ValueError):
            extract_text_from_pdf(b"")

    def test_extract_text_from_docx_invalid_input(self):
        """Test DOCX extraction with invalid input."""
        with pytest.raises(ValueError):
            extract_text_from_docx(None)
        
        with pytest.raises(ValueError):
            extract_text_from_docx(b"")


class TestIntegration:
    """Integration tests for the full pipeline."""
    
    def test_full_analysis_pipeline(self, sample_resume_text, job_description_text):
        """Test the complete analysis pipeline."""
        # Analyze resume
        analyzer = ResumeAnalyzer()
        resume_result = analyzer.analyze(sample_resume_text)
        
        # Calculate job matching
        match_score = calculate_match_score(sample_resume_text, job_description_text)
        missing_keywords = extract_missing_keywords(sample_resume_text, job_description_text)
        suggestions = get_keyword_suggestions(job_description_text)
        
        # Verify all components work together
        assert resume_result['scores']['overall_score'] >= 0
        assert 0 <= match_score <= 100
        assert isinstance(missing_keywords, list)
        assert isinstance(suggestions, dict)
        
        # Integration: high-scoring resumes should have better job matches
        if resume_result['scores']['overall_score'] > 70:
            # Good resumes should typically have some job relevance
            assert match_score > 0 or len(missing_keywords) < 15

    def test_error_handling_integration(self):
        """Test error handling across components."""
        analyzer = ResumeAnalyzer()
        
        # Test with problematic inputs
        problematic_texts = [
            "",  # Empty
            "a",  # Too short
            "x" * 10000,  # Very long
            "!@#$%^&*()",  # Special characters only
        ]
        
        for text in problematic_texts:
            try:
                result = analyzer.analyze(text)
                # Should not crash, should return valid structure
                assert 'scores' in result
                assert 'recommendations' in result
            except (ValueError, RuntimeError):
                # Acceptable to raise these specific exceptions
                pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
    