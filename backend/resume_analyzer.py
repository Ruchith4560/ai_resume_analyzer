import re
import logging
from collections import Counter
from typing import Dict, List, Any
try:
    from .config import skills_config, scoring_config
except ImportError:
    from config import skills_config, scoring_config

logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    """
    Professional resume analyzer with honest, accurate scoring.
    No fake data or inflated scores - provides genuine, actionable feedback.
    """
    
    def __init__(self):
        """Initialize the analyzer with comprehensive skill databases from config."""
        self.technical_skills = skills_config.TECHNICAL_SKILLS
        self.soft_skills = skills_config.SOFT_SKILLS
        self.action_verbs = skills_config.ACTION_VERBS
    
    def analyze(self, resume_text: str) -> Dict[str, Any]:
        """
        Perform honest resume analysis with accurate scoring.
        
        Args:
            resume_text: The extracted text from resume
            
        Returns:
            Dictionary containing genuine analysis results
            
        Raises:
            ValueError: If resume_text is invalid
            RuntimeError: If analysis fails
        """
        if not isinstance(resume_text, str):
            raise ValueError("resume_text must be a string")
            
        if not resume_text or not resume_text.strip():
            return self._get_empty_result()
        
        try:
            clean_text = self._clean_text(resume_text)
            
            # Extract genuine features
            technical_skills = self._extract_technical_skills(clean_text)
            soft_skills = self._extract_soft_skills(clean_text)
            action_verbs = self._extract_action_verbs(clean_text)
            word_freq = self._get_word_frequency(clean_text)
            sections = self._detect_sections(clean_text)
            contact_info = self._extract_contact_info(resume_text)
            
            # Calculate honest scores
            scores = self._calculate_scores(clean_text, resume_text, sections, contact_info)
            
            # Generate genuine recommendations
            recommendations = self._generate_recommendations(
                clean_text, resume_text, scores, technical_skills, 
                soft_skills, action_verbs, sections, contact_info
            )
            
            return {
                'scores': scores,
                'skills': {
                    'technical': technical_skills,
                    'soft': soft_skills
                },
                'technical_skills': technical_skills,
                'soft_skills': soft_skills,
                'action_verbs': action_verbs,
                'action_verbs_count': len(action_verbs),
                'word_count': len(clean_text.split()),
                'word_frequency': dict(list(word_freq.items())[:10]),
                'sections_detected': sections,
                'contact_info': contact_info,
                'recommendations': recommendations
            }
        except Exception as e:
            raise RuntimeError(f"Analysis failed: {str(e)}") from e
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return result for empty input."""
        return {
            'scores': {
                'overall_score': 0,
                'content_quality': 0,
                'keyword_optimization': 0,
                'ats_compatibility': 0,
                'structure_score': 0,
                'completeness': 0
            },
            'skills': {
                'technical': [],
                'soft': []
            },
            'technical_skills': [],
            'soft_skills': [],
            'action_verbs': [],
            'action_verbs_count': 0,
            'word_count': 0,
            'word_frequency': {},
            'sections_detected': [],
            'contact_info': {},
            'recommendations': ['Please upload a valid resume file with content.']
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,@()\-+#&/:]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().lower()
    
    def _extract_technical_skills(self, text: str) -> List[str]:
        """Extract technical skills found in text."""
        found_skills = set()
        for skill in self.technical_skills:
            if re.search(rf'\b{re.escape(skill)}\b', text):
                found_skills.add(skill.title())
        return sorted(list(found_skills))
    
    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills found in text."""
        found_skills = set()
        for skill in self.soft_skills:
            if re.search(rf'\b{re.escape(skill)}\b', text):
                found_skills.add(skill.title())
        return sorted(list(found_skills))
    
    def _extract_action_verbs(self, text: str) -> List[str]:
        """Extract action verbs found in text."""
        found_verbs = []
        for verb in self.action_verbs:
            if re.search(rf'\b{verb}\b', text):
                found_verbs.append(verb)
        return found_verbs
    
    def _get_word_frequency(self, text: str) -> Dict[str, int]:
        """Get word frequency for common important words."""
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'resume', 'cv', 'name', 'address', 'phone', 'email'
        }
        
        words = re.findall(r'\b[a-z]{3,}\b', text)
        filtered_words = [w for w in words if w not in stopwords and len(w) > 3]
        return dict(Counter(filtered_words).most_common(20))
    
    def _detect_sections(self, text: str) -> List[str]:
        """Detect standard resume sections."""
        sections = []
        section_patterns = {
            'Contact': r'\b(contact|phone|email|address|linkedin)\b',
            'Summary': r'\b(summary|profile|objective|about)\b',
            'Experience': r'\b(experience|work|employment|career)\b',
            'Education': r'\b(education|degree|university|college)\b',
            'Skills': r'\b(skills|technical|competencies)\b',
            'Projects': r'\b(projects|portfolio)\b',
            'Certifications': r'\b(certification|certificate|license)\b',
            'Achievements': r'\b(achievement|award|accomplishment)\b'
        }
        
        for section, pattern in section_patterns.items():
            if re.search(pattern, text):
                sections.append(section)
        
        return sections
    
    def _extract_contact_info(self, text: str) -> Dict[str, bool]:
        """Check for contact information."""
        return {
            'has_email': bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)),
            'has_phone': bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)),
            'has_linkedin': bool(re.search(r'linkedin\.com', text, re.IGNORECASE))
        }
    
    def _calculate_scores(self, clean_text: str, original_text: str, 
                         sections: List[str], contact_info: Dict[str, bool]) -> Dict[str, int]:
        """Calculate honest, accurate scores using configuration constants."""
        word_count = len(clean_text.split())
        
        # Content Quality Score (0-100) using config
        content_score = 0
        if scoring_config.OPTIMAL_WORD_COUNT_MIN <= word_count <= scoring_config.OPTIMAL_WORD_COUNT_MAX:
            content_score += 40
        elif (200 <= word_count < scoring_config.OPTIMAL_WORD_COUNT_MIN or 
              scoring_config.OPTIMAL_WORD_COUNT_MAX < word_count <= 900):
            content_score += 30
        elif 100 <= word_count < 200:
            content_score += 20
        else:
            content_score += 10
        
        action_verbs = self._extract_action_verbs(clean_text)
        content_score += min(
            scoring_config.MAX_ACTION_VERB_BONUS, 
            len(action_verbs) * scoring_config.ACTION_VERB_BONUS_POINTS
        )
        
        quantified = len(re.findall(r'\d+%|\d+\+|increased|improved|reduced', clean_text))
        content_score += min(
            scoring_config.MAX_QUANTIFIED_BONUS, 
            quantified * scoring_config.QUANTIFIED_ACHIEVEMENT_BONUS
        )
        # Keyword Optimization Score (0-100) using config
        tech_skills = self._extract_technical_skills(clean_text)
        soft_skills = self._extract_soft_skills(clean_text)
        total_skills = len(tech_skills) + len(soft_skills)
        
        keyword_score = 20  # Base score
        for threshold, score in scoring_config.SKILLS_SCORE_THRESHOLDS.items():
            if total_skills >= threshold:
                keyword_score = score
                break
        else:
            keyword_score = max(20, total_skills * 10)
        
        # ATS Compatibility Score (0-100) using config
        ats_score = 100
        
        missing_sections = [s for s in scoring_config.ESSENTIAL_SECTIONS if s not in sections]
        ats_score -= len(missing_sections) * scoring_config.MISSING_SECTION_PENALTY
        
        if not contact_info.get('has_email'):
            ats_score -= scoring_config.MISSING_EMAIL_PENALTY
        if not contact_info.get('has_phone'):
            ats_score -= scoring_config.MISSING_PHONE_PENALTY
        
        if not re.search(r'\b(19|20)\d{2}\b', clean_text):
            ats_score -= scoring_config.MISSING_DATES_PENALTY
        
        # Structure Score (0-100)
        structure_score = 30  # Base score
        if len(sections) >= 5:
            structure_score = 100
        elif len(sections) >= 4:
            structure_score = 85
        elif len(sections) >= 3:
            structure_score = 70
        else:
            structure_score = max(30, len(sections) * 20)
        
        # Completeness Score (0-100)
        completeness_score = 100
        
        required_elements = {
            'email': contact_info.get('has_email', False),
            'phone': contact_info.get('has_phone', False),
            'experience': 'Experience' in sections,
            'education': 'Education' in sections,
            'skills': 'Skills' in sections
        }
        
        for element, present in required_elements.items():
            if not present:
                if element in ['email', 'phone']:
                    completeness_score -= 15
                else:
                    completeness_score -= 12
        
        # Calculate overall score using config weights
        weights = scoring_config.SCORE_WEIGHTS
        overall_score = int(
            content_score * weights['content_quality'] +
            keyword_score * weights['keyword_optimization'] +
            ats_score * weights['ats_compatibility'] +
            structure_score * weights['structure_score'] +
            completeness_score * weights['completeness']
        )
        
        return {
            'overall_score': max(0, min(100, overall_score)),
            'content_quality': max(0, min(100, content_score)),
            'keyword_optimization': max(0, min(100, keyword_score)),
            'ats_compatibility': max(0, min(100, ats_score)),
            'structure_score': max(0, min(100, structure_score)),
            'completeness': max(0, min(100, completeness_score))
        }
    
    def _generate_recommendations(self, clean_text: str, original_text: str,
                                 scores: Dict[str, int], technical_skills: List[str],
                                 soft_skills: List[str], action_verbs: List[str],
                                 sections: List[str], contact_info: Dict[str, bool]) -> List[str]:
        """
        Generate honest, actionable recommendations based on analysis results.
        
        Args:
            clean_text: Cleaned resume text
            original_text: Original resume text
            scores: Dictionary of calculated scores
            technical_skills: List of detected technical skills
            soft_skills: List of detected soft skills
            action_verbs: List of detected action verbs
            sections: List of detected resume sections
            contact_info: Dictionary of contact information flags
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        word_count = len(clean_text.split())
        
        # Content recommendations
        if scores['content_quality'] < 70:
            if word_count < 200:
                recommendations.append(
                    "Expand your resume content. Add more details about your achievements and responsibilities (aim for 300-600 words)."
                )
            elif word_count > 900:
                recommendations.append(
                    "Condense your resume. Focus on the most impactful achievements and keep it concise."
                )
            
            if len(action_verbs) < 8:
                recommendations.append(
                    "Use more action verbs. Start bullet points with strong verbs like 'Led', 'Developed', 'Implemented', 'Optimized'."
                )
            
            quantified = len(re.findall(r'\d+%|\d+\+|increased|improved|reduced', clean_text))
            if quantified < 3:
                recommendations.append(
                    "Quantify your achievements. Use specific numbers and percentages (e.g., 'Increased sales by 35%')."
                )
        
        # Keyword recommendations
        if scores['keyword_optimization'] < 70:
            if len(technical_skills) < 5:
                recommendations.append(
                    "Add more relevant technical skills. Include programming languages, tools, and technologies you've used."
                )
            if len(soft_skills) < 3:
                recommendations.append(
                    "Highlight soft skills like leadership, communication, teamwork, and problem-solving."
                )
        
        # ATS recommendations
        if scores['ats_compatibility'] < 70:
            essential_sections = ['Experience', 'Education', 'Skills']
            missing = [s for s in essential_sections if s not in sections]
            if missing:
                recommendations.append(
                    f"Add required sections: {', '.join(missing)}. These are essential for ATS systems."
                )
            
            if not contact_info.get('has_email') or not contact_info.get('has_phone'):
                recommendations.append(
                    "Include complete contact information: email and phone number at the top of your resume."
                )
        
        # Structure recommendations
        if scores['structure_score'] < 70:
            recommendations.append(
                "Improve resume structure. Use clear section headings: Contact, Summary, Experience, Education, Skills."
            )
            
            if not re.search(r'\b(19|20)\d{2}\b', clean_text):
                recommendations.append(
                    "Include dates for your work experience and education to show career progression."
                )
        
        # Overall guidance
        if scores['overall_score'] >= 80:
            recommendations.append(
                "Strong resume! Consider tailoring it for specific job descriptions to further improve your match rate."
            )
        elif scores['overall_score'] >= 60:
            recommendations.append(
                "Good foundation. Focus on the specific improvements above to reach the next level."
            )
        else:
            recommendations.append(
                "Focus on the essentials first: clear sections, contact info, work experience with achievements, and relevant skills."
            )
        
        return recommendations[:6]