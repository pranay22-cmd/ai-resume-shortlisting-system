import os
from typing import List
from pydantic import BaseModel
from openai import OpenAI

class AIAnalysis(BaseModel):
    overall_assessment: str
    strengths: List[str]
    weaknesses: List[str]
    skill_gaps: List[str]
    evidence: List[str]
    recommendation: str
    confidence: float

def analyze_resume_with_llm(
        resume_text,
        job_description
):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "overall_assessment": "LLM unavailable",
            "strengths": [],
            "weaknesses": [],
            "skill_gaps": [],
            "evidence": [],
            "recommendation": "Configure OPENAI_API_KEY",
            "confidence": 0.0
        }

    client = OpenAI(api_key=api_key)

    prompt = f"""
Analyze the candidate resume against the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Evaluate only information supported by the resume.

Identify:
1. Overall candidate fit
2. Candidate strengths
3. Candidate weaknesses
4. Skill gaps
5. Evidence from the resume supporting the assessment
6. Hiring recommendation
7. Confidence score from 0 to 100

Do not invent qualifications, experience, skills, projects, education, or achievements.
"""

    completion = client.beta.chat.completions.parse(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI recruitment analysis assistant. "
                    "Analyze resumes objectively and only use evidence "
                    "contained in the supplied resume."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=AIAnalysis
    )

    message = completion.choices[0].message

    if message.parsed:
        return message.parsed.model_dump()

    return {
        "overall_assessment": "LLM analysis unavailable",
        "strengths": [],
        "weaknesses": [],
        "skill_gaps": [],
        "evidence": [],
        "recommendation": "Unable to generate AI assessment",
        "confidence": 0.0
    }