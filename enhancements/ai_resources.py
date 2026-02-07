import json
from openai import OpenAI

client = OpenAI(api_key="sk-abc123")

def generate_resources(curriculum):
    prompt = f"""
For every topic provide:
- free_learning_resource
- practice_project
- reference_material

Short and practical.
Return JSON only.

Curriculum:
{json.dumps(curriculum)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return json.loads(response.choices[0].message.content)
