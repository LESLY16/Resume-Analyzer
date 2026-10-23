def compute_scores(sections, keyword_data):
    section_score = sum(1 for s in sections.values() if len(s) > 50) * 25
    keyword_score = int(keyword_data["match_ratio"] * 100)
    readability_score = compute_readability(sections)

    ats_score = int(0.4 * section_score + 0.4 * keyword_score + 0.2 * readability_score)

    return {
        "ats": ats_score,
        "role_match": keyword_score,
        "readability": readability_score
    }

def compute_readability(sections):
    text = " ".join(sections.values())
    words = text.split()
    if not words:
        return 50

    avg_len = sum(len(w) for w in words) / len(words)
    score = 100 - (avg_len - 4) * 10
    return max(0, min(100, int(score)))
