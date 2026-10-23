from pydantic import BaseModel
from typing import List, Dict

class AnalyzeResponse(BaseModel):
    ats_score: int
    role_match_score: int
    readability_score: int
    sections: Dict[str, str]
    missing_keywords: List[str]
    recommendations: List[str]
