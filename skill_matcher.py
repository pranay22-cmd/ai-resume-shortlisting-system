import re

SKILL_ALIASES = {
    "python": "Python",
    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "data science": "Data Science",
    "data analysis": "Data Analysis",
    "natural language processing": "NLP",
    "nlp": "NLP",
    "artificial intelligence": "Artificial Intelligence",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "scikit-learn": "Scikit-Learn",
    "scikit learn": "Scikit Learn",
    "sklearn" : "Scikit-Learn",
    "sql": "SQL",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "streamlit": "Streamlit",
    "git": "Git",
    "github": "GitHub",
}

def extract_required_skills(job_description):

    text = job_description.lower()

    skills = []

    sorted_skills = sorted(
        SKILL_ALIASES.keys(),
        key=len,
        reverse=True
    )

    for skill in sorted_skills:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):

            normalized_skill = SKILL_ALIASES[skill]

            if normalized_skill not in skills:
                skills.append(normalized_skill)

    return skills


def match_skills(resume_text, required_skills):

    resume_text = resume_text.lower()

    matched_skills = []

    for skill in required_skills:

        skill_lower = skill.lower()

        pattern = r"\b" + re.escape(skill_lower) + r"\b"

        if re.search(pattern, resume_text):
            matched_skills.append(skill)

    return matched_skills


def calculate_skill_score(
    matched_skills,
    required_skills
):

    if not required_skills:
        return 0

    score = (
        len(matched_skills) /
        len(required_skills)
    ) * 100

    return round(score, 2)