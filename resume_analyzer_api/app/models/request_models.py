from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    target_role: str
