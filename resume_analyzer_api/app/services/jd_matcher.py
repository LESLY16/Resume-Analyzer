from app.services.keyword_engine import keyword_present

def calculate_jd_match(
    resume_text: str,
    job_description: str
):
    jd_words = set(
        word.strip().lower()
        for word in job_description.split()
        if len(word.strip()) > 2
    )

    matched = []
    missing = []

    for word in jd_words:

        if keyword_present(resume_text, word):
            matched.append(word)

        else:
            missing.append(word)

    score = 0

    if len(jd_words) > 0:
        score = round(
            (len(matched) / len(jd_words)) * 100
        )

    return {
        "jd_match_score": score,
        "jd_matched_keywords": matched,
        "jd_missing_keywords": missing
    }