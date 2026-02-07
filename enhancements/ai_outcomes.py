import json
from openai import OpenAI

client = OpenAI(api_key="sk-abc123")

def generate_learning_outcomes(curriculum):
    prompt = f"""
Add for each course:
- learning_outcomes
- skills_gained
- career_relevance

Return STRICT JSON only.

Curriculum:
{json.dumps(curriculum)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)
