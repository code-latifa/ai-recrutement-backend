from typing import List, Dict

# Pondérations (modifiable selon la stratégie)
WEIGHTS = {
    'skills': 0.5,
    'experience': 0.3,
    'education': 0.2
}

# Seuils pour la décision (modifiable)
THRESHOLDS = {
    'excellent': 80,
    'good': 65,
    'average': 50
}

def compute_matching_score(candidate: dict, job: dict) -> Dict:
    """
    Calcule un score de matching entre un candidat et une offre.
    Args:
        candidate: dict avec les clés 'skills', 'experience', 'education'
        job: dict avec les clés 'skills', 'experience', 'education'
    Returns:
        dict: {
            'final_score': float,
            'details': { 'skills': float, 'experience': float, 'education': float },
            'decision': str
        }
    """
    # Score compétences (intersection / total requis)
    candidate_skills = set([s.lower() for s in candidate.get('skills', [])])
    job_skills = set([s.lower() for s in job.get('skills', [])])
    if job_skills:
        skills_score = len(candidate_skills & job_skills) / len(job_skills)
    else:
        skills_score = 0.0

    # Score expérience (1 si suffisant, 0.5 si proche, 0 sinon)
    cand_exp = candidate.get('experience', 0)
    job_exp = job.get('experience', 0)
    if cand_exp >= job_exp:
        exp_score = 1.0
    elif cand_exp >= job_exp * 0.7:
        exp_score = 0.5
    else:
        exp_score = 0.0

    # Score éducation (1 si niveau atteint, 0 sinon)
    cand_edu = candidate.get('education', '').lower()
    job_edu = job.get('education', '').lower()
    edu_score = 1.0 if cand_edu == job_edu or not job_edu else 0.0

    # Score final pondéré
    final_score = (
        skills_score * WEIGHTS['skills'] +
        exp_score * WEIGHTS['experience'] +
        edu_score * WEIGHTS['education']
    )
    final_score = round(final_score * 100, 2)  # sur 100

    # Décision simple
    if final_score >= 70:
        decision = "Très bon matching"
    elif final_score >= 50:
        decision = "Matching partiel"
    else:
        decision = "Matching faible"

    return {
        'final_score': final_score,
        'details': {
            'skills': round(skills_score * 100, 2),
            'experience': round(exp_score * 100, 2),
            'education': round(edu_score * 100, 2)
        },
        'decision': decision
    }