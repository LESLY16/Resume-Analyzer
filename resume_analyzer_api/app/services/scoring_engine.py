def compute_scores(sections, keyword_result):
    expected = keyword_result["expected_keywords"]
    found = keyword_result["found_keywords"]
    missing = keyword_result["missing_keywords"]
    match_ratio = keyword_result["match_ratio"]

    # Role Match Score (0–100)
    role_match_score = int(match_ratio * 100)

    # Readability Score (simple heuristic)
    readability_score = 50
    if len(sections.get("experience", "")) > 200:
        readability_score += 20
    if len(sections.get("skills", "")) > 50:
        readability_score += 20
    readability_score = min(readability_score, 100)

    # ATS Score (weighted)
    ats_score = int((role_match_score * 0.6) + (readability_score * 0.4))

    return {
        "ats_score": ats_score,
        "role_match_score": role_match_score,
        "readability_score": readability_score
    }
