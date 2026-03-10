# API Documentation

This document describes the backend API and functions used in the AI Resume Analyzer.

## Table of Contents

- [Resume Analyzer](#resume-analyzer)
- [PDF Extractor](#pdf-extractor)
- [Keyword Matcher](#keyword-matcher)

## Resume Analyzer

Module: `backend.resume_analyzer`

### Class: ResumeAnalyzer

Main class for analyzing resumes using NLP techniques.

#### Constructor

```python
ResumeAnalyzer()
```

Initializes the analyzer with:
- SpaCy NLP model (`en_core_web_sm`)
- Technical skills database
- Soft skills database

#### Methods

##### analyze(resume_text: str) -> Dict[str, Any]

Performs comprehensive resume analysis.

**Parameters:**
- `resume_text` (str): The extracted text from resume

**Returns:**
- Dictionary containing:
  - `overall_score` (int): Overall resume score (0-100)
  - `content_score` (int): Content quality score
  - `keyword_score` (int): Keyword optimization score
  - `ats_score` (int): ATS compatibility score
  - `structure_score` (int): Structure and formatting score
  - `completeness_score` (int): Completeness score
  - `skills` (List[str]): List of identified skills
  - `keywords` (Dict[str, int]): Keyword frequency dictionary
  - `recommendations` (List[str]): Improvement suggestions
  - `word_count` (int): Total word count

**Example:**
```python
from backend.resume_analyzer import ResumeAnalyzer

analyzer = ResumeAnalyzer()
results = analyzer.analyze(resume_text)

print(f"Overall Score: {results['overall_score']}/100")
print(f"Skills Found: {results['skills']}")
```

##### _extract_skills(text: str) -> List[str]

Extracts technical and soft skills from resume text.

**Parameters:**
- `text` (str): Cleaned resume text

**Returns:**
- List[str]: List of identified skills

##### _extract_keywords(text: str) -> Dict[str, int]

Extracts and counts important keywords.

**Parameters:**
- `text` (str): Cleaned resume text

**Returns:**
- Dict[str, int]: Dictionary of keywords and their frequencies

##### _calculate_content_score(text: str) -> int

Calculates content quality score based on word count and structure.

**Scoring Criteria:**
- Ideal word count: 400-800 words (100 points)
- Presence of action verbs (+10 points bonus)
- Overall range: 0-100

**Parameters:**
- `text` (str): Resume text

**Returns:**
- int: Content score (0-100)

##### _calculate_keyword_score(keywords: Dict[str, int]) -> int

Calculates keyword optimization score.

**Scoring Criteria:**
- 15+ unique keywords: 100 points
- 10-14 keywords: 85 points
- 7-9 keywords: 70 points
- <7 keywords: 60 points

**Parameters:**
- `keywords` (Dict[str, int]): Keyword frequency dictionary

**Returns:**
- int: Keyword score (0-100)

##### _calculate_ats_score(text: str) -> int

Calculates ATS (Applicant Tracking System) compatibility score.

**Scoring Criteria:**
- Checks for excessive special characters (-15 points)
- Verifies standard sections (-20 if missing)
- Looks for contact information (-10 if missing)

**Parameters:**
- `text` (str): Resume text

**Returns:**
- int: ATS score (0-100)

##### _calculate_structure_score(text: str) -> int

Calculates resume structure and formatting score.

**Scoring Criteria:**
- Presence of key sections (contact, experience, education, skills)
- Proper chronology with dates
- Standard formatting

**Parameters:**
- `text` (str): Resume text

**Returns:**
- int: Structure score (0-100)

##### _calculate_completeness_score(text: str) -> int

Calculates how complete the resume is.

**Scoring Criteria:**
Checks for essential elements:
- Email address
- Experience indicators
- Education information
- Skills section
- Timeframes/dates

**Parameters:**
- `text` (str): Resume text

**Returns:**
- int: Completeness score (0-100)

##### _generate_recommendations(text: str, skills: List[str], overall_score: int, ats_score: int) -> List[str]

Generates personalized recommendations for resume improvement.

**Parameters:**
- `text` (str): Resume text
- `skills` (List[str]): Identified skills
- `overall_score` (int): Overall score
- `ats_score` (int): ATS score

**Returns:**
- List[str]: List of recommendations (max 6)

---

## PDF Extractor

Module: `backend.pdf_extractor`

### Functions

#### extract_text_from_pdf(pdf_file: Union[BytesIO, bytes]) -> str

Extracts text content from a PDF file.

**Parameters:**
- `pdf_file` (Union[BytesIO, bytes]): PDF file object from Streamlit uploader or bytes

**Returns:**
- str: Extracted text or error message

**Example:**
```python
from backend.pdf_extractor import extract_text_from_pdf

uploaded_file = st.file_uploader("Upload PDF")
if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    print(text)
```

**Error Handling:**
- Returns error message if extraction fails
- Returns message if PDF is image-based

#### get_pdf_metadata(pdf_file: Union[BytesIO, bytes]) -> dict

Extracts metadata from a PDF file.

**Parameters:**
- `pdf_file` (Union[BytesIO, bytes]): PDF file object

**Returns:**
- Dictionary containing:
  - `num_pages` (int): Number of pages
  - `author` (str): Document author
  - `title` (str): Document title
  - `subject` (str): Document subject
  - `error` (str): Error message if extraction fails

**Example:**
```python
from backend.pdf_extractor import get_pdf_metadata

metadata = get_pdf_metadata(pdf_file)
print(f"Pages: {metadata['num_pages']}")
```

---

## Keyword Matcher

Module: `backend.keyword_matcher`

### Functions

#### calculate_match_score(resume_text: str, job_description: str) -> int

Calculates the match score between a resume and job description.

**Algorithm:**
1. Uses TF-IDF vectorization
2. Calculates cosine similarity
3. Adds bonus for important keyword matches
4. Returns final score (0-100)

**Parameters:**
- `resume_text` (str): Text extracted from resume
- `job_description` (str): Job description text

**Returns:**
- int: Match score (0-100)

**Example:**
```python
from backend.keyword_matcher import calculate_match_score

score = calculate_match_score(resume_text, job_description)
print(f"Job Match: {score}%")
```

#### extract_missing_keywords(resume_text: str, job_description: str) -> List[str]

Finds keywords present in job description but missing from resume.

**Parameters:**
- `resume_text` (str): Resume text
- `job_description` (str): Job description text

**Returns:**
- List[str]: List of missing keywords (max 10)

**Example:**
```python
from backend.keyword_matcher import extract_missing_keywords

missing = extract_missing_keywords(resume_text, job_description)
print(f"Missing keywords: {missing}")
```

#### get_keyword_suggestions(job_description: str) -> Dict[str, List[str]]

Gets keyword suggestions based on job description.

**Parameters:**
- `job_description` (str): Job description text

**Returns:**
- Dictionary containing:
  - `technical_skills` (List[str]): Technical skills found
  - `soft_skills` (List[str]): Soft skills found
  - `action_verbs` (List[str]): Action verbs found

**Example:**
```python
from backend.keyword_matcher import get_keyword_suggestions

suggestions = get_keyword_suggestions(job_description)
print(f"Technical Skills: {suggestions['technical_skills']}")
print(f"Soft Skills: {suggestions['soft_skills']}")
print(f"Action Verbs: {suggestions['action_verbs']}")
```

---

## Data Models

### Analysis Result

```python
{
    'overall_score': int,          # 0-100
    'content_score': int,          # 0-100
    'keyword_score': int,          # 0-100
    'ats_score': int,             # 0-100
    'structure_score': int,        # 0-100
    'completeness_score': int,     # 0-100
    'skills': List[str],           # ['Python', 'Java', ...]
    'keywords': Dict[str, int],    # {'python': 5, 'java': 3, ...}
    'recommendations': List[str],  # ['Add more skills', ...]
    'word_count': int,             # Total words
    'match_score': int             # Optional, 0-100
}
```

### Skills Database

The analyzer uses predefined skill databases:

**Technical Skills:**
- Programming Languages: Python, Java, JavaScript, C++, etc.
- Frameworks: React, Django, Flask, Spring, etc.
- Tools: Docker, Kubernetes, Git, Jenkins, etc.
- Databases: MongoDB, PostgreSQL, MySQL, etc.
- Concepts: Machine Learning, NLP, Cloud Computing, etc.

**Soft Skills:**
- Leadership, Communication, Teamwork
- Problem Solving, Critical Thinking
- Project Management, Collaboration
- Analytical, Decision Making

---

## Error Handling

All functions include error handling:

- PDF extraction errors return descriptive error messages
- Missing or invalid input returns appropriate defaults
- Score calculations are bounded (0-100)
- Empty text inputs are handled gracefully

## Performance Considerations

- SpaCy model loaded once during initialization
- Caching recommended for repeated analyses
- TF-IDF vectorization may be slow for very long texts
- Consider batch processing for multiple resumes

## Future API Extensions

Planned additions:
- Support for DOCX format
- Multi-language support
- Industry-specific scoring
- Custom skill database configuration
- Batch analysis endpoint

---

Last updated: December 2026
