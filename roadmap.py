import requests

HUGGINGFACE_API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
    "Content-Type": "application/json"
}

def generate_roadmap(name: str, skills: str, goal: str) -> str:
    prompt = f"""
You are a career mentor AI. A student named {name} is asking for a personalized learning roadmap.

Current skills: {skills}
Career goal: {goal}

Generate a detailed, friendly, and structured roadmap for {name} that includes:
- Learning phases: Beginner, Intermediate, Advanced
- Important topics to learn in each phase
- Suggested tools, platforms, and courses
- Mini projects or activities to build practical experience
- Estimated timelines (in weeks)
- Any relevant certifications

Keep the tone motivating and clear.
"""

    data = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"].replace(prompt, "").strip()
    else:
        return f"⚠️ Error generating roadmap: {response.status_code} - {response.text}"
