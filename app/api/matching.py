
"""
API Endpoints pour le matching CV-Offre
Membre 5 - Niveau 2
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.matching import (
    MatchingRequest,
    MatchingResponse,
    SearchMatchingRequest,
    MatchingListResponse
)
from app.ai.moteur_matching import executer_matching, executer_matching_avec_recherche
from app.ai.embeddings import embed_text


router = APIRouter(prefix="/matching", tags=["Matching"])


# ============================================
# MATCHING SIMPLE : 1 CV vs 1 OFFRE
# ============================================

@router.post("/score", response_model=MatchingResponse)
async def calculer_matching(
    request: MatchingRequest,
    db: Session = Depends(get_db)
):
    """
    Calcule le score de matching entre un CV et une offre.
    
    Retourne :
    - Score final (0-100)
    - Détails par critère
    - Explications IA pour recruteur et candidat
    """
    try:
        # Récupérer le CV depuis la base
        from app.models.cv import CV
        cv = db.query(CV).filter(CV.id == request.cv_id).first()
        
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CV {request.cv_id} introuvable"
            )
        
        # Récupérer l'offre depuis la base
        from app.models.offre_emploi import OffreEmploi
        offre = db.query(OffreEmploi).filter(OffreEmploi.id == request.offre_id).first()
        
        if not offre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Offre {request.offre_id} introuvable"
            )
        
        # Exécuter le matching
        resultat = executer_matching(
            cv_json=cv.json_structure,
            offre_json=offre.json_structure,
            cv_embedding=cv.embedding,
            offre_embedding=offre.embedding,
            generer_explications=request.generer_explications
        )
        
        return MatchingResponse(**resultat)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du matching : {str(e)}"
        )


# ============================================
# MATCHING AVANCÉ : 1 CV vs TOUTES LES OFFRES
# ============================================

@router.post("/search-offres", response_model=MatchingListResponse)
async def rechercher_meilleures_offres(
    request: SearchMatchingRequest,
    db: Session = Depends(get_db)
):
    """
    Trouve les meilleures offres pour un CV donné.
    
    Utilise ChromaDB pour une recherche vectorielle rapide.
    """
    try:
        # Récupérer le CV
        from app.models.cv import CV
        cv = db.query(CV).filter(CV.id == request.cv_id).first()
        
        if not cv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CV {request.cv_id} introuvable"
            )
        
        # Récupérer toutes les offres actives
        from app.models.offre_emploi import OffreEmploi
        offres = db.query(OffreEmploi).filter(OffreEmploi.statut == "active").all()
        
        if not offres:
            return MatchingListResponse(
                cv_id=request.cv_id,
                matches=[],
                total_results=0
            )
        
        # Exécuter le matching pour chaque offre
        matches = []
        
        for offre in offres[:request.top_k]:  # Limiter au top_k
            resultat = executer_matching(
                cv_json=cv.json_structure,
                offre_json=offre.json_structure,
                cv_embedding=cv.embedding,
                offre_embedding=offre.embedding,
                generer_explications=request.generer_explications
            )
            
            matches.append(MatchingResponse(**resultat))
        
        # Trier par score décroissant
        matches.sort(key=lambda x: x.score_final, reverse=True)
        
        return MatchingListResponse(
            cv_id=request.cv_id,
            matches=matches[:request.top_k],
            total_results=len(matches)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la recherche : {str(e)}"
        )


# ============================================
# MATCHING INVERSE : 1 OFFRE vs TOUS LES CV
# ============================================

@router.post("/search-candidats/{offre_id}", response_model=MatchingListResponse)
async def rechercher_meilleurs_candidats(
    offre_id: str,
    top_k: int = 10,
    generer_explications: bool = True,
    db: Session = Depends(get_db)
):
    """
    Trouve les meilleurs candidats pour une offre donnée.
    
    Utile pour les recruteurs qui veulent voir les CV les plus pertinents.
    """
    try:
        # Récupérer l'offre
        from app.models.offre_emploi import OffreEmploi
        offre = db.query(OffreEmploi).filter(OffreEmploi.id == offre_id).first()
        
        if not offre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Offre {offre_id} introuvable"
            )
        
        # Récupérer tous les CV
        from app.models.cv import CV
        cvs = db.query(CV).all()
        
        if not cvs:
            return MatchingListResponse(
                offre_id=offre_id,
                matches=[],
                total_results=0
            )
        
        # Exécuter le matching pour chaque CV
        matches = []
        
        for cv in cvs:
            resultat = executer_matching(
                cv_json=cv.json_structure,
                offre_json=offre.json_structure,
                cv_embedding=cv.embedding,
                offre_embedding=offre.embedding,
                generer_explications=generer_explications
            )
            
            matches.append(MatchingResponse(**resultat))
        
        # Trier par score décroissant
        matches.sort(key=lambda x: x.score_final, reverse=True)
        
        return MatchingListResponse(
            offre_id=offre_id,
            matches=matches[:top_k],
            total_results=len(matches)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la recherche : {str(e)}"
        )


# ============================================
# ENDPOINT DE TEST
# ============================================

@router.post("/test")
async def tester_matching(
    cv_json: dict,
    offre_json: dict,
    generer_explications: bool = True
):
    """
    Endpoint de test pour le matching sans accès à la base de données.
    
    Permet de tester le moteur de matching avec des données JSON directes.
    """
    try:
        resultat = executer_matching(
            cv_json=cv_json,
            offre_json=offre_json,
            generer_explications=generer_explications
        )
        
        return MatchingResponse(**resultat)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du test : {str(e)}"
        )
