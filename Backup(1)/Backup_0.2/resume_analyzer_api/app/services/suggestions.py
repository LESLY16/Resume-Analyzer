def generate_suggestions(sections, keyword_data):
    suggestions = []

    if len(sections["summary"]) < 80:
        suggestions.append("Improve your summary with measurable achievements.")

    if keyword_data["missing"]:
        suggestions.append("Add missing keywords: " + ", ".join(keyword_data["missing"]))

    if len(sections["experience"]) < 150:
        suggestions.append("Expand your experience section with bullet points.")

    return suggestions