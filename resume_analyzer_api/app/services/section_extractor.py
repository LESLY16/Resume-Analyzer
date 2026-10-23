import re
from datetime import datetime

# Universal headings for resumes
SECTION_HEADERS = {
    "summary": [
        "summary", "professional summary", "profile", "about me",
        "objective", "career objective", "overview"
    ],
    "skills": [
        "skills", "technical skills", "tech stack", "core skills",
        "skills & abilities", "competencies", "key skills"
    ],
    "experience": [
        "experience", "work experience", "professional experience",
        "employment history", "work history", "career history",
        "projects", "project experience"
    ],
    "education": [
        "education", "academics", "qualifications", "certifications",
        "education & certifications", "academic background"
    ]
}

def build_regex():
    all_headers = []
    for group in SECTION_HEADERS.values():
        all_headers.extend(group)

    header_regex = "|".join([re.escape(h) for h in all_headers])

    pattern = rf"(?P<header>{header_regex})[:\s\n-]*?(?P<content>[\s\S]*?)(?=\n\s*(?:{header_regex})[:\s\n-]|$)"

    return re.compile(pattern, re.IGNORECASE)

SECTION_PATTERN = build_regex()


# ---------------------------
# EXPERIENCE DURATION LOGIC
# ---------------------------

DATE_PATTERNS = [
    r"(\b\d{4}\b)",  # year only
    r"(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b)",  # Month YYYY
]

MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

def parse_date(text):
    text = text.lower().strip()

    # Month YYYY
    for m in MONTH_MAP:
        if text.startswith(m):
            year = int(text.split()[-1])
            return datetime(year, MONTH_MAP[m], 1)

    # Year only
    if text.isdigit() and len(text) == 4:
        return datetime(int(text), 1, 1)

    return None


def calculate_experience_duration(experience_text):
    dates = []

    for pattern in DATE_PATTERNS:
        matches = re.findall(pattern, experience_text, re.IGNORECASE)
        for m in matches:
            d = parse_date(m)
            if d:
                dates.append(d)

    if len(dates) < 2:
        return 0  # Not enough dates to calculate duration

    start = min(dates)
    end = max(dates)

    years = (end - start).days / 365
    return round(years, 1)


# ---------------------------
# BULLET POINT DETECTION
# ---------------------------

def extract_bullets(text):
    bullets = re.findall(r"[-•●]\s+(.*)", text)
    return bullets


# ---------------------------
# MAIN SECTION EXTRACTION
# ---------------------------

def extract_sections(text: str):
    sections = {
        "summary": "",
        "skills": "",
        "experience": "",
        "education": "",
        "experience_years": 0,
        "experience_bullets": []
    }

    matches = SECTION_PATTERN.finditer(text)

    for match in matches:
        header = match.group("header").lower().strip()
        content = match.group("content").strip()

        for section_name, header_list in SECTION_HEADERS.items():
            if header in [h.lower() for h in header_list]:
                sections[section_name] = content

                # Special processing for experience section
                if section_name == "experience":
                    sections["experience_years"] = calculate_experience_duration(content)
                    sections["experience_bullets"] = extract_bullets(content)

    return sections