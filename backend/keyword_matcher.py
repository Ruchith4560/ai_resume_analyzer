import re
from typing import Dict, List, Set, Union
from collections import Counter
import logging

logger = logging.getLogger(__name__)

def calculate_match_score(resume_text: str, job_description: str) -> int:
    """
    Calculate the match score between a resume and job description using keyword matching.
    
    Args:
        resume_text: Text extracted from resume
        job_description: Job description text
        
    Returns:
        Match score as integer (0-100)
        
    Raises:
        ValueError: If inputs are invalid
    """
    if not isinstance(resume_text, str) or not isinstance(job_description, str):
        raise ValueError("Both resume_text and job_description must be strings")
        
    if not resume_text.strip() or not job_description.strip():
        return 0
    
    try:
        # Clean texts
        resume_clean = _clean_text(resume_text)
        job_clean = _clean_text(job_description)
        
        # Calculate keyword overlap score
        base_score = _keyword_overlap_score(resume_clean, job_clean)
        
        # Bonus for matching important keywords
        important_keywords = _extract_important_keywords(job_clean)
        matched_keywords = sum(1 for keyword in important_keywords if keyword in resume_clean)
        
        if important_keywords:
            keyword_bonus = min(20, (matched_keywords / len(important_keywords)) * 20)
        else:
            keyword_bonus = 0
        
        final_score = min(100, base_score + int(keyword_bonus))
        
        return max(0, final_score)
    
    except Exception as e:
        logger.error(f"Error calculating match score: {e}")
        return 0


def _clean_text(text: str) -> str:
    """Clean and normalize text for comparison."""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters except spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _keyword_overlap_score(resume_text: str, job_text: str) -> int:
    """
    Calculate match score based on keyword overlap.
    
    Args:
        resume_text: Cleaned resume text
        job_text: Cleaned job description text
        
    Returns:
        Score as integer (0-100)
    """
    # Simple stopwords
    stopwords = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would'
    }
    
    # Extract words
    resume_words = set(word for word in resume_text.split() 
                      if word not in stopwords and len(word) > 2)
    job_words = set(word for word in job_text.split() 
                   if word not in stopwords and len(word) > 2)
    
    if not job_words:
        return 0
    
    # Calculate overlap
    overlap = len(resume_words.intersection(job_words))
    score = int((overlap / len(job_words)) * 100)
    
    return min(100, score)


def _extract_important_keywords(job_text: str) -> List[str]:
    """
    Extract important keywords from job description.
    
    Args:
        job_text: Cleaned job description text
        
    Returns:
        List of important keywords
    """
    # Technical and business keywords that are often important
    important_terms = {
        # Programming languages
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'go',
        'typescript', 'kotlin', 'swift', 'rust', 'scala', 'r',
        
        # Frameworks and libraries
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        
        # Technologies
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'git',
        'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
        
        # Concepts
        'machine learning', 'deep learning', 'nlp', 'computer vision',
        'data science', 'artificial intelligence', 'blockchain',
        'cloud computing', 'devops', 'agile', 'scrum', 'microservices',
        
        # Soft skills
        'leadership', 'communication', 'teamwork', 'problem solving',
        'project management', 'analytical', 'collaboration'
    }
    
    # Find which important terms appear in job description
    found_keywords = []
    job_lower = job_text.lower()
    
    for term in important_terms:
        if term in job_lower:
            found_keywords.append(term)
    
    return found_keywords


def extract_missing_keywords(resume_text: str, job_description: str) -> List[str]:
    """
    Find keywords present in job description but missing from resume.
    
    Args:
        resume_text: Text from resume
        job_description: Job description text
        
    Returns:
        List of missing keywords (top 10)
        
    Raises:
        ValueError: If inputs are invalid
    """
    if not isinstance(resume_text, str) or not isinstance(job_description, str):
        raise ValueError("Both inputs must be strings")
    
    if not resume_text.strip() or not job_description.strip():
        return []
    
    try:
        resume_clean = _clean_text(resume_text)
        job_clean = _clean_text(job_description)
        
        job_keywords = _extract_important_keywords(job_clean)
        
        missing = [keyword for keyword in job_keywords if keyword not in resume_clean]
        
        return missing[:10]  # Return top 10 missing keywords
    
    except Exception as e:
        logger.error(f"Error extracting missing keywords: {e}")
        return []


def get_keyword_suggestions(job_description: str) -> Dict[str, List[str]]:
    """
    Get keyword suggestions based on job description.
    
    Args:
        job_description: Job description text
        
    Returns:
        Dictionary with categorized keyword suggestions
        
    Raises:
        ValueError: If job_description is invalid
    """
    if not isinstance(job_description, str):
        raise ValueError("job_description must be a string")
    
    if not job_description.strip():
        return {'technical_skills': [], 'soft_skills': [], 'action_verbs': []}
    
    try:
        job_clean = _clean_text(job_description)
        
        suggestions = {
            'technical_skills': [],
            'soft_skills': [],
            'action_verbs': []
        }
        
        # Technical skills to check
        technical = [
            'python', 'java', 'javascript', 'react', 'angular', 'docker',
            'kubernetes', 'aws', 'machine learning', 'sql', 'git'
        ]
        
        # Soft skills to check
        soft = [
            'leadership', 'communication', 'teamwork', 'analytical',
            'problem solving', 'project management'
        ]
        
        # Action verbs
        actions = [
            'developed', 'managed', 'led', 'designed', 'implemented',
            'created', 'improved', 'analyzed', 'coordinated'
        ]
        
        for skill in technical:
            if skill in job_clean:
                suggestions['technical_skills'].append(skill.title())
        
        for skill in soft:
            if skill in job_clean:
                suggestions['soft_skills'].append(skill.title())
        
        for verb in actions:
            if verb in job_clean:
                suggestions['action_verbs'].append(verb.title())
        
        return suggestions
    
    except Exception as e:
        logger.error(f"Error getting keyword suggestions: {e}")
        return {'technical_skills': [], 'soft_skills': [], 'action_verbs': []}