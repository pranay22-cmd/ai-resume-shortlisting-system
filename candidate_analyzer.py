import re


def extract_education(resume_text):
    education_patterns = [
        "b.tech",
        "btech",
        "b.e",
        "be",
        "m.tech",
        "mtech",
        "m.e",
        "me",
        "bca",
        "mca",
        "b.sc",
        "bsc",
        "m.sc",
        "msc",
        "bachelor",
        "master",
        "computer science",
        "information technology",
        "artificial intelligence",
        "data science"
    ]

    resume_lower = resume_text.lower()

    education = []

    for education_item in education_patterns:
        if education_item in resume_lower:
            education.append(education_item)

    return education


def calculate_education_score(
    resume_text,
    required_education
):
    if not required_education:
        return 100.0

    resume_lower = resume_text.lower()

    matched = 0

    for education in required_education:
        if education.lower() in resume_lower:
            matched += 1

    score = (
        matched / len(required_education)
    ) * 100

    return round(score, 2)


def analyze_candidate(
    resume_text,
    required_skills,
    matched_skills
):
    required_set = set(required_skills)
    matched_set = set(matched_skills)

    missing_skills = sorted(
        required_set - matched_set
    )

    skill_coverage = 0

    if required_skills:
        skill_coverage = (
            len(matched_skills) /
            len(required_skills)
        ) * 100

    strengths = []

    if matched_skills:
        strengths.append(
            f"Matches {len(matched_skills)} required skill(s)."
        )

    if skill_coverage >= 80:
        strengths.append(
            "Strong technical skill coverage."
        )

    elif skill_coverage >= 50:
        strengths.append(
            "Moderate technical skill coverage."
        )

    else:
        strengths.append(
            "Limited coverage of required skills."
        )

    weaknesses = []

    if missing_skills:
        weaknesses.append(
            "Missing required skills: "
            + ", ".join(missing_skills)
        )

    else:
        weaknesses.append(
            "No major required skill gaps detected."
        )

    return {
        "Matched Skills": matched_skills,
        "Missing Skills": missing_skills,
        "Skill Coverage": round(skill_coverage, 2),
        "Strengths": strengths,
        "Weaknesses": weaknesses
    }
