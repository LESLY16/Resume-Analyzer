from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.services.visitor_counter import get_count, increment_count
from app.auth.api_key_validator import validate_api_key
from app.models.response_models import AnalyzeResponse
from app.services.file_parser import extract_text
from app.services.section_extractor import extract_sections
from app.services.keyword_engine import compute_keyword_matches
from app.services.scoring_engine import compute_scores
from app.services.suggestions import generate_suggestions

app = FastAPI(title="Resume Analyzer API")

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    target_role: str,
    file: UploadFile = File(...),
    api_key: str = Depends(validate_api_key)
):
    text = await extract_text(file)
    sections = extract_sections(text)
    keyword_data = compute_keyword_matches(text, target_role)
    scores = compute_scores(sections, keyword_data)
    suggestions = generate_suggestions(sections, keyword_data)

    return AnalyzeResponse(
        ats_score=scores["ats"],
        role_match_score=scores["role_match"],
        readability_score=scores["readability"],
        sections=sections,
        missing_keywords=keyword_data["missing"],
        recommendations=suggestions
    )

@app.get("/visitor-count")
def visitor_count():
    return {"count": get_count()}

@app.get("/visitor-count/increment")
def visitor_increment():
    new_count = increment_count()
    return {"count": new_count}
