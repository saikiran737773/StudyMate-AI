import requests

HUGGINGFACE_API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
    "Content-Type": "application/json"
}

def analyze_resume(resume_text: str, job_description: str = "") -> str:
    if job_description:
        prompt = f"""
You are an advanced ATS bot that reviews resumes for a job opening.

Resume:
{resume_text}

Job Description:
{job_description}

Analyze the resume based on:
- Matching skills and experiences
- Strengths
- Weaknesses or missing info
- Improvements to get shortlisted

Give a structured, clear response. Be concise and helpful.
"""
    else:
        prompt = f"""
You are an advanced ATS bot. Analyze the following resume and give:

- Key strengths and skills
- Weak points or missing sections
- Suggestions to improve for better job matching
- ATS-friendliness score out of 10

Resume:
{resume_text}

Respond in a structured and friendly tone.
"""

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.json()[0]["generated_text"].replace(prompt, "").strip()
    else:
        return f"⚠️ Error analyzing resume: {response.status_code} - {response.text}"
