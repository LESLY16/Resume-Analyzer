from pydantic import BaseModel
from typing import List, Dict, Any


class AnalysisResponse(BaseModel):
    ats_score: int
    role_match_score: int
    readability_score: int
    missing_keywords: List[str]
    recommendations: List[str]
    sections: Dict[str, Any]
