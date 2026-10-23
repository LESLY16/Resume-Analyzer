import re

def extract_sections(text: str):
    sections = {
        "summary": "",
        "experience": "",
        "skills": "",
        "education": ""
    }

    patterns = {
        "summary": r"(summary|profile|about me)(.*?)(experience|skills|education)",
        "experience": r"(experience|work history)(.*?)(skills|education)",
        "skills": r"(skills)(.*?)(education|projects)",
        "education": r"(education)(.*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[key] = match.group(2).strip()

    return sections
