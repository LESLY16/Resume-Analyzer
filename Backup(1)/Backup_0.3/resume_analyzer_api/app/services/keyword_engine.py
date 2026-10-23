import json
import re

with open("app/data/role_keywords.json") as f:
    ROLE_KEYWORDS = json.load(f)

def compute_keyword_matches(text: str, role: str):
    keywords = ROLE_KEYWORDS.get(role.lower(), [])
    found = []
    missing = []

    for kw in keywords:
        if re.search(rf"\b{kw}\b", text, re.IGNORECASE):
            found.append(kw)
        else:
            missing.append(kw)

    return {
        "found": found,
        "missing": missing,
        "match_ratio": len(found) / len(keywords) if keywords else 0
    }
