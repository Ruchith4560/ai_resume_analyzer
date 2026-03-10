"""
Configuration management for AI Resume Analyzer
"""
import os
from typing import Dict, List

class Config:
    """Base configuration class."""
    
    # Application Settings
    APP_NAME: str = os.getenv('APP_NAME', 'AI Resume Analyzer')
    APP_VERSION: str = os.getenv('APP_VERSION', '2.0.0')
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # API Configuration
    API_HOST: str = os.getenv('API_HOST', 'localhost')
    API_PORT: int = int(os.getenv('API_PORT', '8000'))
    API_WORKERS: int = int(os.getenv('API_WORKERS', '1'))
    
    # File Upload Settings
    MAX_FILE_SIZE_MB: int = int(os.getenv('MAX_FILE_SIZE_MB', '5'))
    ALLOWED_EXTENSIONS: List[str] = os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx,txt').split(',')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your_secret_key_here')
    CORS_ORIGINS: List[str] = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Feature Flags
    ENABLE_JOB_MATCHING: bool = os.getenv('ENABLE_JOB_MATCHING', 'True').lower() == 'true'
    ENABLE_ATS_ANALYSIS: bool = os.getenv('ENABLE_ATS_ANALYSIS', 'True').lower() == 'true'
    ENABLE_PREMIUM_FEATURES: bool = os.getenv('ENABLE_PREMIUM_FEATURES', 'False').lower() == 'true'
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    RATE_LIMIT_PER_HOUR: int = int(os.getenv('RATE_LIMIT_PER_HOUR', '1000'))
    
    # Cache Settings
    CACHE_TTL_SECONDS: int = int(os.getenv('CACHE_TTL_SECONDS', '3600'))
    REDIS_URL: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

class SkillsConfig:
    """Configuration for skills detection."""
    
    TECHNICAL_SKILLS = {
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 
        'swift', 'kotlin', 'go', 'rust', 'scala', 'r', 'sql', 'html', 'css',
        'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'fastapi', 
        'spring', 'laravel', 'mysql', 'postgresql', 'mongodb', 'redis', 
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git',
        'machine learning', 'data analysis', 'tensorflow', 'pytorch'
    }
    
    SOFT_SKILLS = {
        'leadership', 'communication', 'teamwork', 'problem solving',
        'critical thinking', 'adaptability', 'time management', 'creativity',
        'attention to detail', 'project management', 'collaboration'
    }
    
    ACTION_VERBS = {
        'achieved', 'developed', 'designed', 'implemented', 'created', 'built',
        'led', 'managed', 'improved', 'optimized', 'increased', 'reduced',
        'analyzed', 'collaborated', 'presented', 'delivered', 'established',
        'founded', 'launched', 'supervised', 'coordinated', 'trained'
    }

class ScoringConfig:
    """Configuration for scoring algorithms."""
    
    # Content Quality Scoring
    OPTIMAL_WORD_COUNT_MIN = 300
    OPTIMAL_WORD_COUNT_MAX = 700
    ACTION_VERB_BONUS_POINTS = 2
    QUANTIFIED_ACHIEVEMENT_BONUS = 5
    MAX_ACTION_VERB_BONUS = 30
    MAX_QUANTIFIED_BONUS = 30
    
    # Keyword Optimization Scoring
    SKILLS_SCORE_THRESHOLDS = {
        15: 100,
        10: 85,
        7: 70,
        5: 55,
        3: 40
    }
    
    # ATS Compatibility Scoring
    ESSENTIAL_SECTIONS = ['Experience', 'Education', 'Skills']
    MISSING_SECTION_PENALTY = 25
    MISSING_EMAIL_PENALTY = 15
    MISSING_PHONE_PENALTY = 10
    MISSING_DATES_PENALTY = 10
    
    # Overall Score Weights
    SCORE_WEIGHTS = {
        'content_quality': 0.25,
        'keyword_optimization': 0.20,
        'ats_compatibility': 0.25,
        'structure_score': 0.15,
        'completeness': 0.15
    }

# Initialize configuration
config = Config()
skills_config = SkillsConfig()
scoring_config = ScoringConfig()