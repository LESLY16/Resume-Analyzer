from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.auth.api_key_validator import validate_api_key
from app.models.response_models import AnalysisResponse
from app.services.file_parser import parse_file
from app.services.section_extractor import extract_sections
from app.services.keyword_engine import analyze_keywords, ROLE_KEYWORDS
from app.services.scoring_engine import compute_scores
from app.services.suggestions import generate_resume_suggestions

app = FastAPI()

# CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://resume-analyzer-1-jccr.onrender.com"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running"}


@app.get("/roles")
def get_roles():
    return {"roles": list(ROLE_KEYWORDS.keys())}


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    target_role: str,
    file: UploadFile = File(...),
    api_key: str = Depends(validate_api_key),
):
    # Validate role
    allowed_roles = list(ROLE_KEYWORDS.keys())

    if target_role.lower() not in allowed_roles:
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Role '{target_role}' is not available.",
                "available_roles": allowed_roles
            }
        )

    # Validate file type
    allowed_extensions = (".pdf", ".docx")
    if not (file.filename or "").lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF or DOCX."
        )

    # Continue with normal flow...
    text = await parse_file(file)

    # ---------------------------------------------------------
    # FINAL FIX: SCANNED / UNEDITABLE / INCOMPATIBLE RESUME CHECK
    # ---------------------------------------------------------

    # Case 1: No text extracted → scanned or protected PDF
    if not text or len(text.strip()) == 0:
        raise HTTPException(
            status_code=400,
            detail="Resume is incompatible or uneditable. Please upload a text-based PDF or DOCX file."
        )

    # Case 2: Very short text → image-only PDF or unreadable content
    if len(text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Resume is incompatible or scanned. Please upload a text-based PDF or DOCX file."
        )

    # Case 3: Text contains mostly non-alphabetic garbage → encrypted/protected PDF
    alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)
    if alpha_ratio < 0.05:  # less than 5% readable characters
        raise HTTPException(
            status_code=400,
            detail="Resume appears to be protected or uneditable. Please upload a text-based PDF or DOCX file."
        )

    # Extract sections
    sections = extract_sections(text)

    # If sections are empty or meaningless → scanned/incompatible resume
    if not sections or all(not str(v).strip() for v in sections.values()):
        raise HTTPException(
            status_code=400,
            detail="Resume is incompatible or scanned. Please upload a text-based PDF or DOCX file."
        )

    # Keyword analysis
    keyword_result = analyze_keywords(target_role, text)

    # Role exists but has no keywords configured
    if not keyword_result["expected_keywords"]:
        raise HTTPException(
            status_code=400,
            detail=f"Role '{target_role}' is valid but has no keywords configured. Please update role_keywords.json."
        )

    # Compute scores
    scores = compute_scores(sections, keyword_result)

    # Suggestions
    suggestions = generate_resume_suggestions(
        keyword_result["missing_keywords"],
        sections,
        scores["readability_score"],
        scores["ats_score"],
        scores["role_match_score"]
    )

    # Final response
    return AnalysisResponse(
        ats_score=scores["ats_score"],
        role_match_score=scores["role_match_score"],
        readability_score=scores["readability_score"],
        missing_keywords=keyword_result["missing_keywords"],
        recommendations=suggestions,
        sections=sections,
    )
