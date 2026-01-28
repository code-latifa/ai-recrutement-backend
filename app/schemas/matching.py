from pydantic import BaseModel
from typing import Dict

class MatchResponse(BaseModel):
    candidate_id: int
    job_id: int
    final_score: float
    details: Dict[str, float]
    decision: str
    explanation: str
