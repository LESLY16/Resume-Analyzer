def generate_resume_suggestions(
    missing_keywords: list[str],
    sections: dict,
    readability_score: int,
    ats_score: int,
    role_match_score: int
):
    suggestions = []

    # ---------------------------------------------------------
    # Missing Keywords
    # ---------------------------------------------------------
    if missing_keywords:
        suggestions.append(
            f"Add missing role-specific keywords: {', '.join(missing_keywords)}."
        )

    # ---------------------------------------------------------
    # Missing Sections (FINAL FIX APPLIED HERE)
    # ---------------------------------------------------------
    missing_sections = []

    for name, value in sections.items():
        # Handle None
        if value is None:
            missing_sections.append(name)
            continue

        # Convert non-string values
        if not isinstance(value, str):
            value = str(value)

        # Check empty or whitespace
        if not value.strip():
            missing_sections.append(name)

    if missing_sections:
        suggestions.append(
            f"Add or improve missing sections: {', '.join(missing_sections)}."
        )

    # ---------------------------------------------------------
    # Readability Improvements
    # ---------------------------------------------------------
    if readability_score < 60:
        suggestions.append(
            "Improve readability by using bullet points, consistent formatting, and shorter sentences."
        )

    # ---------------------------------------------------------
    # ATS Score Improvements
    # ---------------------------------------------------------
    if ats_score < 50:
        suggestions.append(
            "Increase ATS score by adding clear headings, consistent formatting, and more structured content."
        )

    # ---------------------------------------------------------
    # Role Match Improvements
    # ---------------------------------------------------------
    if role_match_score < 50:
        suggestions.append(
            "Increase role match by adding more relevant experience, projects, and skills aligned with the target role."
        )

    # ---------------------------------------------------------
    # Final fallback
    # ---------------------------------------------------------
    if not suggestions:
        suggestions.append("Your resume looks strong. Only minor refinements may be needed.")

    return suggestions
