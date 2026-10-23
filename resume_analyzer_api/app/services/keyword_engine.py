import json
import os
from app.services.semantic_keywords import SEMANTIC_SYNONYMS

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "role_keywords.json"
)

def load_role_keywords():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

ROLE_KEYWORDS = load_role_keywords()


def keyword_present(text: str, keyword: str) -> bool:
    text_lower = text.lower()
    kw_lower = keyword.lower()

    # Direct match
    if kw_lower in text_lower:
        return True

    # Semantic match
    if kw_lower in SEMANTIC_SYNONYMS:
        for synonym in SEMANTIC_SYNONYMS[kw_lower]:
            if synonym.lower() in text_lower:
                return True

    return False


def analyze_keywords(target_role: str, text: str):
    role = target_role.lower().strip()

    role_data = ROLE_KEYWORDS.get(role, {})
    expected_keywords = role_data.get("keywords", [])

    found = []
    missing = []

    text_lower = text.lower()

    for kw in expected_keywords:
        if keyword_present(text_lower, kw):
            found.append(kw)
        else:
            missing.append(kw)

    match_ratio = len(found) / len(expected_keywords) if expected_keywords else 0

    return {
        "expected_keywords": expected_keywords,
        "found_keywords": found,
        "missing_keywords": missing,
        "match_ratio": match_ratio
    }
