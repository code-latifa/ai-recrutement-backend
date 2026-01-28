from app.services.matching_service import match_candidate_to_job
from app.schemas.matching import MatchResponse

def build_explanation_prompt(data: dict) -> str:
    """
    Construit un prompt pour l'IA d'explication du matching.
    """
    return f"""
You are an HR assistant.

Candidate skills: {data.get('skills', [])}
Job required skills: {data.get('job_skills', [])}
Experience score: {data.get('details', {}).get('experience', 0)}
Education score: {data.get('details', {}).get('education', 0)}
Final score: {data.get('final_score', 0)}
Decision: {data.get('decision', '')}

Explain clearly and professionally the matching result. Give advice if needed.
"""

def generate_matching_and_explanation(candidate: dict, job: dict, ia_explainer=None) -> MatchResponse:
    """
    Calcule le matching, génère l'explication IA (optionnelle) et retourne la réponse complète.
    """
    match = match_candidate_to_job(candidate, job)
    # Préparer les données pour le prompt
    prompt_data = {
        'skills': candidate.get('skills', []),
        'job_skills': job.get('skills', []),
        'details': match.details,
        'final_score': match.final_score,
        'decision': match.decision
    }
    prompt = build_explanation_prompt(prompt_data)
    explanation = ""
    if ia_explainer:
        explanation = ia_explainer(prompt)
    else:
        # Fallback simple si pas d'IA
        explanation = f"Score: {match.final_score}/100. Decision: {match.decision}."
    match.explanation = explanation
    return match
