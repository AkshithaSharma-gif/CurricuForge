import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "granite3.3:2b"

def generate_curriculum(skill, education_level, semesters, weekly_hours, industry_focus):

    prompt = f"""
Create an industry aligned academic curriculum.

Skill: {skill}
Education Level: {education_level}
Duration: {semesters} semesters
Weekly Hours: {weekly_hours}
Industry Focus: {industry_focus}

Return ONLY valid JSON:

{{
  "program": "{skill} Curriculum",
  "semesters": [
    {{
      "semester": 1,
      "courses": [
        {{
          "course_name": "Course Name",
          "topics": ["Topic 1", "Topic 2", "Topic 3"]
        }}
      ]
    }}
  ]
}}

No explanations. JSON only.
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        res.raise_for_status()
        result = res.json()
        return json.loads(result["response"])
    except Exception as e:
        return {"error": str(e)}











