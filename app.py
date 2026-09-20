import os
import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from resume_parser import extract_text
from semantic_matcher import semantic_similarity
from candidate_analyzer import (
    analyze_candidate,
    calculate_education_score
    )
from job_analyzer import analyze_job_description
from scoring import calculate_final_score, get_recommendation
from skill_matcher import (
    extract_required_skills,
    match_skills,
    calculate_skill_score
)


st.set_page_config(
    page_title="AI Resume Shortlisting",
    page_icon="🤖",
    layout="wide"
)


with open("job_description.txt", "r", encoding="utf-8") as file:
    job_description = file.read()


required_skills = extract_required_skills(
    job_description
)

job_analysis = analyze_job_description(
    job_description
)


st.title("🤖 AI Resume Shortlisting System")

st.write(
    "Intelligent resume screening and candidate ranking using NLP and Machine Learning."
)

st.divider()


with st.sidebar:

    st.header("⚙️ Job Information")

    st.subheader("Job Description")

    st.info(job_description)

    st.subheader(" Job Role")

    if job_analysis["Job Role"]:
        st.write(job_analysis["Job Role"])
    else:
        st.write("Not deetected")

    st.subheader("Experience")
    if job_analysis["Experience"]:
        st.write(job_analysis["Experience"])
    else:
        st.write("Not detected")

    st.subheader("🎓 Education")

if job_analysis["Education"]:
    st.write(job_analysis["Education"])
else:
    st.write("Not detected")

st.subheader("🔑 Job Keywords")

if job_analysis["Keywords"]:
    for keyword in job_analysis["Keywords"]:
        st.write(f"• {keyword}")
else:
    st.write("No keywords detected")

    st.subheader("Required Skills")

    for skill in required_skills:
        st.write(f"✓ {skill}")


st.subheader("📄 Upload Resumes")


uploaded_files = st.file_uploader(
    "Choose PDF, DOCX or TXT resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)


analyze = st.button(
    "🚀 Analyze All Resumes",
    use_container_width=True
)


if analyze:

    resume_folder = "resumes"

    os.makedirs(
        resume_folder,
        exist_ok=True
    )

    candidates = []
    resumes = []

    existing_files = set()

    for filename in os.listdir(resume_folder):

        if filename.lower().endswith(
            (".txt", ".pdf", ".docx")
        ):

            filepath = os.path.join(
                resume_folder,
                filename
            )

            resume = extract_text(filepath)

            if resume and resume.strip():

                candidates.append(filename)

                resumes.append(resume)

                existing_files.add(filename)


    if uploaded_files:

        for uploaded_file in uploaded_files:

            filename = uploaded_file.name

            file_path = os.path.join(
                resume_folder,
                filename
            )

            with open(
                file_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )

            resume = extract_text(
                file_path
            )

            if resume and resume.strip():

                if filename not in existing_files:

                    candidates.append(
                        filename
                    )

                    resumes.append(
                        resume
                    )


    if not resumes:

        st.error(
            "❌ No resumes found."
        )

        st.stop()


    documents = [
        job_description
    ] + resumes


    vectorizer = TfidfVectorizer()


    vectors = vectorizer.fit_transform(
        documents
    )


    job_vector = vectors[0]

    resume_vectors = vectors[1:]


    text_scores = cosine_similarity(
        job_vector,
        resume_vectors
    )[0]


    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "machine learning",
        "data science",
        "software engineer",
        "data analyst"
    ]


    results = []


    for candidate, resume, text_score in zip(
        candidates,
        resumes,
        text_scores
    ):

        resume_lower = resume.lower()


        match_percentage = (
            text_score * 100
        )


        matched_skills = match_skills(
            resume,
            required_skills
        )


        skill_score = calculate_skill_score(
            matched_skills,
            required_skills
        )


        candidate_analysis = analyze_candidate(
            resume,
            required_skills,
            matched_skills
        )

        education_score = calculate_education_score(
            resume,
            job_analysis["Required Education"]
        )

        semantic_score = semantic_similarity(
            resume,
            job_description
        )


        experience_match = 0


        for keyword in experience_keywords:

            if keyword in resume_lower:

                experience_match += 20


        experience_match = min(
            experience_match,
            100
        )


        final_score = calculate_final_score(
            match_percentage,
            skill_score,
            semantic_score,
            experience_match
        )


        status, recommendation = get_recommendation(
            final_score
        )


        results.append({

            "Candidate": candidate,

            "Text Match": round(
                match_percentage,
                2
            ),

            "Skills Match": round(
                skill_score,
                2
            ),

            "Semantic Match": round(
                semantic_score,
                2
            ),

            "Experience Match": round(
                experience_match,
                2
            ),

            "Final Score": round(
                final_score,
                2
            ),

            "Skills Matched": ", ".join(
                candidate_analysis[
                    "Matched Skills"
                ]
            ),

            "Missing Skills": ", ".join(
                candidate_analysis[
                    "Missing Skills"
                ]
            ),

            "Skill Coverage": round(
                candidate_analysis[
                    "Skill Coverage"
                ],
                2
            ),

            "Strengths": "; ".join(
                candidate_analysis[
                    "Strengths"
                ]
            ),

            "Weaknesses": "; ".join(
                candidate_analysis[
                    "Weaknesses"
                ]
            ),

            "Status": status,

            "Recommendation": recommendation
        })


    results.sort(
        key=lambda x: x["Final Score"],
        reverse=True
    )


    shortlisted = sum(
        1
        for result in results
        if result["Status"] == "SHORTLISTED"
    )


    maybe = sum(
        1
        for result in results
        if result["Status"] == "MAYBE"
    )


    rejected = sum(
        1
        for result in results
        if result["Status"] == "REJECTED"
    )


    st.subheader(
        "📊 Shortlisting Summary"
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "👥 Total Candidates",
        len(results)
    )


    col2.metric(
        "✅ Shortlisted",
        shortlisted
    )


    col3.metric(
        "🟡 Maybe",
        maybe
    )


    col4.metric(
        "❌ Rejected",
        rejected
    )


    st.divider()


    st.subheader(
        "🏆 Candidate Ranking"
    )


    table_data = []


    for rank, result in enumerate(
        results,
        start=1
    ):

        table_data.append({

            "Rank": rank,

            "Candidate": result[
                "Candidate"
            ],

            "Text Match": (
                f'{result["Text Match"]:.2f}%'
            ),

            "Skills Match": (
                f'{result["Skills Match"]:.2f}%'
            ),

            "Semantic AI": (
                f'{result["Semantic Match"]:.2f}%'
            ),

            "Experience": (
                f'{result["Experience Match"]:.2f}%'
            ),

            "Final Score": (
                f'{result["Final Score"]:.2f}%'
            ),

            "Status": result[
                "Status"
            ]
        })


    df = pd.DataFrame(
        table_data
    )


    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


    st.subheader(
        "📈 Candidate Score Comparison"
    )


    chart_data = pd.DataFrame({

        "Candidate": [
            result["Candidate"]
            for result in results
        ],

        "Final Score": [
            result["Final Score"]
            for result in results
        ]

    })


    chart_data = chart_data.set_index(
        "Candidate"
    )


    st.bar_chart(
        chart_data
    )


    st.subheader(
        "🔍 Candidate Details"
    )
    for rank, result in enumerate(results, start=1):

     with st.expander(
        f'#{rank} — {result["Candidate"]} — {result["Final Score"]:.2f}%'
    ):

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f'**Text Match:** {result["Text Match"]:.2f}%'
            )

            st.write(
                f'**Skills Match:** {result["Skills Match"]:.2f}%'
            )

            st.write(
                f'**Semantic AI Match:** {result["Semantic Match"]:.2f}%'
            )

            st.write(
                f'**Experience Match:** {result["Experience Match"]:.2f}%'
            )

            st.write(
                f'**Skill Coverage:** {result["Skill Coverage"]:.2f}%'
            )

        with col2:

            st.write(
                f'**Final Score:** {result["Final Score"]:.2f}%'
            )

            if result["Status"] == "SHORTLISTED":
                st.success(result["Status"])

            elif result["Status"] == "MAYBE":
                st.warning(result["Status"])

            else:
                st.error(result["Status"])

            st.write(
                f'**Recommendation:** {result["Recommendation"]}'
            )

        st.divider()

        st.write("### ✅ Matched Skills")

        if result["Skills Matched"]:
            st.success(result["Skills Matched"])
        else:
            st.warning("No required skills matched.")

        st.write("### ⚠️ Missing Skills")

        if result["Missing Skills"]:
            st.warning(result["Missing Skills"])
        else:
            st.success("No required skills missing.")

        st.write("### 💪 Strengths")

        if result["Strengths"]:
            for strength in result["Strengths"].split(";"):
                st.write(f"• {strength.strip()}")
        else:
            st.write("No major strengths detected.")

        st.write("### ⚠️ Weaknesses")

        if result["Weaknesses"]:
            for weakness in result["Weaknesses"].split(";"):
                st.write(f"• {weakness.strip()}")
        else:
            st.write("No major weaknesses detected.")


    st.subheader(
        "📥 Export Results"
    )


    download_df = pd.DataFrame(
        results
    )


    csv = download_df.to_csv(
        index=False
    )


    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="resume_shortlisting_results.csv",
        mime="text/csv",
        use_container_width=True
    )


    st.success(
        "✅ Resume analysis completed successfully!"
    )