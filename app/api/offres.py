from typing import Any, Dict, Optional, Union
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.vector_store.indexing import index_offer, search_cvs_for_offer


router = APIRouter(prefix="/offres", tags=["Offres"])


class OffreIndexRequest(BaseModel):
    offre_id: str = Field(..., examples=["offre_1"])
    offre: Union[Dict[str, Any], str]
    metadata: Optional[Dict[str, Any]] = None


class OffreSearchCVRequest(BaseModel):
    offre: Union[Dict[str, Any], str]
    top_k: int = 10


@router.post("/index")
def index_offre(payload: OffreIndexRequest):
    """
    Indexe une offre (JSON ou texte) dans la collection Chroma des offres.
    """
    index_offer(payload.offre_id, payload.offre, payload.metadata)
    return {"status": "ok", "indexed_id": payload.offre_id}


@router.post("/search-cvs")
def search_cvs(payload: OffreSearchCVRequest):
    """
    À partir d'une offre (JSON ou texte), retourne les Top-N CVs (collection cvs).
    """
    result = search_cvs_for_offer(payload.offre, top_k=payload.top_k)
    return result
