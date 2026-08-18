import os
import requests
from dotenv import load_dotenv

load_dotenv()
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def _fallback_explanation(top_result, profile):
    career = top_result["career"]
    reasons = top_result["reasons"]
    first = f"{career['name']} is your strongest match at {top_result['score']}%."
    body = " ".join(reasons) + "."
    gap = profile.get("skill_gap", {})
    if gap.get("missing"):
        body += " Your next priority should be " + ", ".join(gap["missing"][:4]) + "."
    return first + " " + body


def generate_explanation(top_result, profile):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _fallback_explanation(top_result, profile), False

    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    prompt = f"""
You are an educational career guidance assistant. Give a concise, encouraging,
evidence-based explanation of why the recommended career fits this student's
assessment. Do not claim certainty, diagnosis, or guaranteed employment/salary.
Use only the supplied data.

Student profile:
{profile}

Recommendation:
{top_result}

Write 2 short paragraphs and one short "Next step" sentence.
""".strip()

    payload = {
        "model": model,
        "input": prompt,
        "max_output_tokens": 250
    }
    try:
        response = requests.post(
            f"{base_url}/responses",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=20
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("output_text", "").strip()
        if not text:
            for item in data.get("output", []):
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        text += content.get("text", "")
        if text.strip():
            return text.strip(), True
    except Exception:
        pass
    return _fallback_explanation(top_result, profile), False
