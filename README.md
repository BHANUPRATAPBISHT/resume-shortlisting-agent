# resume-shortlisting-agent
using python &amp; openAi
# AI Resume Shortlisting Agent

## 📌 Description
This project is an AI-powered resume shortlisting system that compares a resume with a job description.

## ⚙️ How it works
- Takes resume and job description as input
- Compares skills, experience, education, and projects
- Calculates match percentage
- If match >= 70% → Shortlisted
- Else → Rejected

## 📊 Output
Returns JSON:
```json
{
  "decision": "Shortlisted",
  "match_percentage": 75,
  "reason": "Matched skills include Python, SQL, and HTML"
}
