from fastapi import APIRouter
from app.ai.moteur_matching import generate_matching_and_explanation
from app.schemas.matching import MatchResponse

router = APIRouter(prefix="/matching", tags=["Matching"])

@router.post("/match", response_model=MatchResponse)
def match_endpoint(payload: dict):
    """
    Endpoint API : reçoit un candidat et une offre, retourne score + explication IA.
    """
    candidate = payload.get("candidate", {})
    job = payload.get("job", {})
    # Appel avec fallback (pas d'IA réelle ici, mais prêt pour LLM)
    result = generate_matching_and_explanation(candidate, job)
    return result
