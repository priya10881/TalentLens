import os
import json
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def analyze_resume(resume_text):
    prompt = f"""
You are a resume-parsing assistant.

Extract these fields:
- candidateName
- email
- skills (list of strings)
- education
- experienceYears (number; use 0 if not specified)

Rules:
1. Use only information present in the resume.
2. If a text field is missing, return an empty string.
3. Return only valid JSON.

Resume text:
{resume_text}
"""

    models = [
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.8-flash",
    ]

    last_error = None

    for model in models:
        try:
            print(f"Trying model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={"response_mime_type": "application/json"},
            )

            return json.loads(response.text)

        except Exception as error:
            last_error = error
            print(f"Model failed: {error}")

    raise RuntimeError(f"All models failed: {last_error}")


if __name__ == "__main__":
    sample_resume = """
    Alex Morgan
    Email: alex.morgan@example.com
    Skills: Python, AWS, SQL
    Education: BSc Computer Science
    Experience: 2 years as a Python developer
    """

    result = analyze_resume(sample_resume)
    print(json.dumps(result, indent=2))
