from llm_analyzer import analyze_resume_with_llm

resume = """
Rahul Sharma

Education:
B.Tech in Computer Science

Skills:
Python, Machine Learning, Pandas, NumPy, SQL, Scikit-Learn

Projects:
Built a machine learning model for house price prediction.
Created a data analysis project using Python and Pandas.

Experience:
6 month internship in Data Science.

Certifications:
Python for Data Science
Machine Learning Fundamentals
"""

job_description = """
We are looking for a Junior Machine Learning Engineer.

Requirements:
Python
Machine Learning
Scikit-Learn
Pandas
NumPy
SQL

Experience with machine learning projects and data science is preferred.
"""

result = analyze_resume_with_llm(
    resume,
    job_description
)

print("\nLLM ANALYSIS\n")
print(result)
