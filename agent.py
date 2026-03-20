import json
import re
import openai
from openai import OpenAI

# 🔑 put your NEW API key here (inside quotes)
# NOTE: if you get quota errors, you can still use the local match percentage.
client = OpenAI(api_key="your_open_ai_key")


def _normalize_text(text: str) -> set[str]:
    """Normalize text into a set of lowercase keyword tokens."""
    tokens = re.split(r"\W+", text.lower())
    return {t for t in tokens if len(t) > 1}


def _compute_match_percentage(resume: str, jd: str) -> int:
    """Compute a simple match percentage between JD and resume keywords."""
    jd_terms = _normalize_text(jd)
    resume_terms = _normalize_text(resume)
    if not jd_terms:
        return 0

    overlap = jd_terms & resume_terms
    return round(100 * len(overlap) / len(jd_terms))


def _reason_from_ai(resume: str, jd: str, match_percentage: int) -> str:
    """Get a short explanation for why the resume matches the JD.

    If the OpenAI API call fails (e.g., quota errors), fallback to a plain-text explanation.
    """
    prompt = f"""
You are an assistant that evaluates how well a resume matches a job description.

Resume:
{resume}

Job Description:
{jd}

Based on skills, experience, education, and projects, briefly explain why this candidate is a good or poor fit.
Include the computed match percentage ({match_percentage}%) in your explanation.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # Fallback if OpenAI is not available (quota, key missing, etc.)
        return (
            f"Unable to fetch a human-readable reason from OpenAI (error: {e}). "
            f"Computed match percentage is {match_percentage}% based on keyword overlap."
        )


def shortlist(resume: str, jd: str) -> dict:
    """Return a JSON-able dict with decision, match_percentage, and reason."""
    match_percentage = _compute_match_percentage(resume, jd)
    decision = "Shortlisted" if match_percentage >= 70 else "Rejected"

    reason = _reason_from_ai(resume, jd, match_percentage)

    return {
        "decision": decision,
        "match_percentage": match_percentage,
        "reason": reason,
    }

if __name__ == "__main__":
    print("1. Use sample data")
    print("2. Enter your own data")

    choice = input("Choose option (1 or 2): ")

    if choice == "1":
        # ✅ SAMPLE DATA
        resume = """
        Python developer with experience in Django, Flask, SQL, HTML, CSS.
        Built web applications and REST APIs.
        """

        jd = """
        Looking for Python backend developer with Django or Flask,
        strong SQL skills, and experience in web applications.
        """

    else:
        # ✅ USER INPUT
        print("\nEnter Resume:")
        resume = input()

        print("\nEnter Job Description:")
        jd = input()

    result = shortlist(resume, jd)
    print("\nResult:")
    print(json.dumps(result, indent=2))
