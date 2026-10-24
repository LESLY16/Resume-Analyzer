from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class AnalysisResponse(BaseModel):
    ats_score: int
    role_match_score: int
    readability_score: int
    missing_keywords: List[str]
    recommendations: List[str]
    sections: Dict[str, Any]

    # NEW FIELDS
    jd_match_score: Optional[int] = None
    jd_matched_keywords: Optional[List[str]] = []
    jd_missing_keywords: Optional[List[str]] = []
