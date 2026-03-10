"""
Pytest configuration and fixtures for AI Resume Analyzer tests
"""
import pytest
import sys
import os
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

@pytest.fixture
def sample_resume_text():
    """Sample resume text for testing."""
    return """
    John Doe
    Software Engineer
    john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe
    
    PROFESSIONAL SUMMARY
    Experienced software engineer with 5+ years developing scalable applications
    
    EXPERIENCE
    Senior Software Engineer | Tech Company | 2021-Present
    • Developed microservices using Python and FastAPI, improving system performance by 40%
    • Led team of 5 developers in agile environment
    • Implemented CI/CD pipelines using Docker and Jenkins
    
    Software Engineer | StartupCo | 2019-2021
    • Built React frontend applications served by Node.js backend
    • Collaborated with product team to deliver features on time
    • Optimized database queries, reducing load times by 25%
    
    EDUCATION
    Bachelor of Science in Computer Science | University of Technology | 2019
    
    TECHNICAL SKILLS
    Languages: Python, JavaScript, TypeScript, SQL
    Frameworks: React, Django, FastAPI, Node.js
    Tools: Docker, Jenkins, Git, AWS, PostgreSQL
    
    SOFT SKILLS
    Leadership, Communication, Problem Solving, Team Collaboration
    """

@pytest.fixture
def minimal_resume_text():
    """Minimal resume text for testing edge cases."""
    return """
    Jane Smith
    Developer
    jane@email.com
    
    Experience:
    Worked at a company doing programming.
    
    Education:
    Computer Science degree.
    """

@pytest.fixture
def empty_resume_text():
    """Empty resume text for testing error handling."""
    return ""

@pytest.fixture
def job_description_text():
    """Sample job description for matching tests."""
    return """
    We are seeking a Senior Python Developer to join our team.
    
    Requirements:
    - 5+ years experience with Python development
    - Experience with FastAPI, Django, or Flask
    - Knowledge of AWS cloud services
    - Experience with Docker and containerization
    - Strong communication and leadership skills
    - Experience with React and JavaScript is a plus
    - Database experience with PostgreSQL or MySQL
    
    You will be responsible for:
    - Developing scalable backend applications
    - Leading technical initiatives
    - Mentoring junior developers
    - Collaborating with cross-functional teams
    """

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment."""
    # Set test environment variables
    os.environ['DEBUG'] = 'True'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    
    yield
    
    # Cleanup if needed
    pass