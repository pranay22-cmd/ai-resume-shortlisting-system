import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from resume_parser import extract_text

with open("job_description.txt", "r", encoding="utf-8") as file:
    job_description = file.read()

required_skills = []

lines = job_description.splitlines()

inside_requirements = False

for line in lines:

    line = line.strip()

    if line.lower() == "requirements:":
        inside_requirements = True
        continue

    if inside_requirements:

        if line == "":
            continue

        if line.lower().startswith("the candidate"):
            break

        if line.lower().startswith("experience"):
            break

        required_skills.append(line.lower())

resume_folder = "resumes"

candidates = []
resumes = []

for filename in os.listdir(resume_folder):

    if filename.lower().endswith((".txt", ".pdf", ".docx")):

        filepath = os.path.join(resume_folder, filename)

        resume = extract_text(filepath)

        candidates.append(filename)
        resumes.append(resume)

documents = [job_description] + resumes

vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(documents)

job_vector = vectors[0]

resume_vectors = vectors[1:]

scores = cosine_similarity(job_vector, resume_vectors)[0]


print("AI Resume Shortlisting System")
print("===================================")

results = []

for candidate, resume, score in zip(candidates, resumes, scores):

    match_percentage = score * 100

    matched_skills = []

    for skill in required_skills:
        if skill in resume.lower():
            matched_skills.append(skill)

    if len(required_skills) > 0:
        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        skill_score = 0

    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "machine learning",
        "data science",
        "software engineer",
        "data analyst"
    ]

    experience_match = 0

    for keyword in experience_keywords:
        if keyword in resume.lower():
            experience_match += 20

    if experience_match > 100:
        experience_match = 100

    final_score = (
        (match_percentage * 0.30)
        + (skill_score * 0.50)
        + (experience_match * 0.20)
    )

    results.append(
        (
            candidate,
            match_percentage,
            skill_score,
            experience_match,
            final_score,
            matched_skills
        )
    )

results.sort(
    key=lambda x: x[4],
    reverse=True
)

print("\nCandidate Ranking:")
print("-----------------------------------")


for rank, (
    candidate,
    score,
    skill_score,
    experience_match,
    final_score,
    matched_skills
) in enumerate(results, start=1):


    if final_score >= 70:

        status = "SHORTLISTED"
        recommendation = "Strong Match"


    elif final_score >= 50:

        status = "MAYBE"
        recommendation = "Moderate Match"


    else:

        status = "REJECTED"
        recommendation = "Poor Match"


    print(f"{rank}. {candidate}")
    print(f" Text Match Score: {score:.2f}%")
    print(f" Skills Match Score: {skill_score:.2f}%")
    print(f" Experience Match: {experience_match:.2f}%")
    print(f" Final Score : {final_score:.2f}%")
    print(f" Skills Matched:{', '.join(matched_skills)}")
    print(f" Status : {status}")
    print(f"Recommendation:{recommendation}")
    print()


shortlisted = 0
maybe = 0
rejected = 0

for (
    candidate,
    score,
    skill_score,
    experience_match,
    final_score,
    matched_skills
) in results:


    if final_score >= 70:

        shortlisted += 1


    elif final_score >= 50:

        maybe += 1


    else:

        rejected += 1

print("===================================")
print("SHORTLISTING SUMMARY")
print("===================================")
print(f"Total Candidates: {len(results)}")
print(f"Shortlisted:{shortlisted}")
print(f"Maybe:{maybe}")
print(f"Rejected:{rejected}")
print("===================================")