import re


def extract_required_education(job_description):
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

    text = job_description.lower()
    education = []

    for education_item in education_patterns:
        pattern = r"\b" + re.escape(education_item) + r"\b"

        if re.search(pattern, text):
            if education_item not in education:
                education.append(education_item)

    return education


def analyze_job_description(job_description):
    text = job_description.lower()

    result = {
        "Job Role": "",
        "Required Skills": [],
        "Preferred Skills": [],
        "Experience": "",
        "Education": "",
        "Required Education": [],
        "Keywords": []
    }

    role_match = re.search(
        r"(?:job title|position|role)\s*:\s*(.+)",
        job_description,
        re.IGNORECASE
    )

    if role_match:
        result["Job Role"] = role_match.group(1).strip()

    required_match = re.search(
        r"requirements\s*:\s*(.*?)(?=\n\s*(?:preferred|experience|education|the candidate)|$)",
        job_description,
        re.IGNORECASE | re.DOTALL
    )

    if required_match:
        required_text = required_match.group(1)

        result["Required Skills"] = [
            skill.strip().title()
            for skill in re.split(r"[,;\n]+", required_text)
            if skill.strip()
        ]

    preferred_match = re.search(
        r"preferred\s*(?:skills|qualifications)?\s*:\s*(.*?)(?=\n\s*(?:experience|education|requirements|the candidate)|$)",
        job_description,
        re.IGNORECASE | re.DOTALL
    )

    if preferred_match:
        preferred_text = preferred_match.group(1)

        result["Preferred Skills"] = [
            skill.strip().title()
            for skill in re.split(r"[,;\n]+", preferred_text)
            if skill.strip()
        ]

    experience_match = re.search(
        r"(?:experience|work experience)\s*:\s*(.*?)(?=\n\s*(?:education|preferred|requirements)|$)",
        job_description,
        re.IGNORECASE | re.DOTALL
    )

    if experience_match:
        result["Experience"] = experience_match.group(1).strip()

    education_match = re.search(
        r"(?:education|qualification)\s*:\s*(.*?)(?=\n\s*(?:experience|preferred|requirements)|$)",
        job_description,
        re.IGNORECASE | re.DOTALL
    )

    if education_match:
        result["Education"] = education_match.group(1).strip()

    keyword_patterns = [
        "python",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data science",
        "data analysis",
        "nlp",
        "natural language processing",
        "pandas",
        "numpy",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "sql",
        "git",
        "github",
        "streamlit"
    ]

    for keyword in keyword_patterns:
        if re.search(
            r"\b" + re.escape(keyword) + r"\b",
            text
        ):
            result["Keywords"].append(keyword.title())

    result["Required Education"] = extract_required_education(
        job_description
    )

    return result


if __name__ == "__main__":
    with open(
        "job_description.txt",
        "r",
        encoding="utf-8"
    ) as file:
        job_description = file.read()

    analysis = analyze_job_description(
        job_description
    )

    print("\nJOB ANALYSIS")
    print("=" * 40)

    print(
        "Job Role:",
        analysis["Job Role"]
    )

    print(
        "Required Skills:",
        analysis["Required Skills"]
    )

    print(
        "Preferred Skills:",
        analysis["Preferred Skills"]
    )

    print(
        "Experience:",
        analysis["Experience"]
    )

    print(
        "Education:",
        analysis["Education"]
    )

    print(
        "Required Education:",
        analysis["Required Education"]
    )

    print(
        "Keywords:",
        analysis["Keywords"]
    )