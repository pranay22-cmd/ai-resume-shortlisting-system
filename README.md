# 🤖 AI Resume Shortlisting System

An advanced, AI-powered resume screening and candidate ranking system designed to streamline recruitment. By leveraging **Natural Language Processing (NLP)**, **Semantic Similarity**, and **Large Language Models (LLMs)**, this system efficiently analyzes candidate resumes against specific job descriptions to generate an objective, ranked shortlist.

---

## 🚀 Key Features

* **📄 Intelligent Resume Parsing:** Automatically extracts structured text and key details from various resume formats.
* **💼 Job Description Analysis:** Breaks down requirements, responsibilities, and qualifications from the target job description.
* **🔍 Precision Skill Matching:** Compares candidate skill sets directly against mandatory and preferred job requirements.
* **🧠 Semantic Similarity Analysis:** Uses advanced vector embeddings to understand context beyond simple keyword matching.
* **📊 Multi-Factor Scoring:** Combines semantic matching, experience relevance, and skill alignment into a unified score.
* **🏆 Ranked Shortlisting:** Outputs a neatly organized, prioritized list of top candidates for recruiters.
* **🤖 LLM-Based Insights:** Deepens candidate evaluation using Large Language Models for qualitative analysis.
* **🧪 Testing & Validation:** Includes dedicated test modules to verify the reliability of core analysis components.

---

## 🛠️ Tech Stack & Libraries

* **Core Language:** Python
* **Backend Framework:** FastAPI / Python standard app components
* **AI & NLP:** Large Language Models (LLMs), Semantic Text Matching, Text Processing pipelines
* **Utilities:** Resume Parsing libraries, Machine Learning utilities

---

## ⚙️ How It Works

1. **Input Ingestion:** The target job description (`job_description.txt`) and a batch of candidate resumes are fed into the system.
2. **Text Extraction:** `resume_parser.py` parses unstructured files into clean, readable text.
3. **Requirement Extraction:** `job_analyzer.py` isolates critical skills and experience benchmarks.
4. **Comparative Analysis:** 
   * `skill_matcher.py` cross-references candidate skills with job needs.
   * `semantic_matcher.py` computes contextual alignment using semantic embeddings.
5. **Scoring & Ranking:** `scoring.py` aggregates metrics to calculate a final weighted score for every candidate.
6. **Output Generation:** The system delivers a ranked shortlist to accelerate decision-making.

---

## 📁 Project Structure

```text
AI-Resume-Shortlisting-System/
│
├── app.py                  # Web application entry point / API routes
├── main.py                 # Core execution script
├── candidate_analyzer.py   # Processes and evaluates individual candidate profiles
├── job_analyzer.py         # Parses and structures job descriptions
├── job_description.txt     # Sample input file for target job requirements
├── llm_analyzer.py         # Integrates LLM logic for deep qualitative analysis
├── resume_parser.py        # Extracts text and metadata from resumes
├── scoring.py              # Calculates final multi-factor candidate scores
├── semantic_matcher.py     # Computes semantic similarity embeddings
├── skill_matcher.py        # Performs keyword and skill overlap analysis
├── test_llm.py             # Unit tests for LLM functionality
├── requirements.txt        # Project dependencies
└── .gitignore              # Files and directories to ignore by Git

## 💻 Installation

Clone the repository:

```bash
git clone https://github.com/pranay22-cmd/ai-resume-shortlisting-system.git
cd ai-resume-shortlisting-system

## ▶️ Running the Project

Run the application using:

```bash
python app.py
