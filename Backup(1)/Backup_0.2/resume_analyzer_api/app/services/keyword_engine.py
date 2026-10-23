import json
import os
import re

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "role_keywords.json")

with open(DATA_PATH, encoding="utf-8") as f:
    ROLE_KEYWORDS = json.load(f)

def compute_keyword_matches(text: str, role: str):
    role_key = role.lower().strip()

    # Fuzzy role matching
    keywords = ROLE_KEYWORDS.get(role_key)
    if not keywords:
        for k in ROLE_KEYWORDS.keys():
            if role_key in k or k in role_key:
                keywords = ROLE_KEYWORDS[k]
                break

    if not keywords:
        keywords = ROLE_KEYWORDS["software developer"]  # fallback

    found, missing = [], []

    for kw in keywords:
        if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
            found.append(kw)
        else:
            missing.append(kw)

    ratio = len(found) / len(keywords)

    return {"found": found, "missing": missing, "match_ratio": ratio}
