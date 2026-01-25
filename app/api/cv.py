from typing import Any, Dict, Optional, Union
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.vector_store.indexing import index_cv_from_json, search_offres_for_cv


router = APIRouter(prefix="/cvs", tags=["CVs"])


class CVIndexRequest(BaseModel):
    cv_id: str = Field(..., examples=["cv_1"])
    cv_json: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class CVSearchOffresRequest(BaseModel):
    cv_json: Dict[str, Any]
    top_k: int = 10


@router.post("/index")
def index_cv(payload: CVIndexRequest):
    """
    Indexe un CV (JSON) dans la collection Chroma des CVs.
    """
    index_cv_from_json(payload.cv_id, payload.cv_json, payload.metadata)
    return {"status": "ok", "indexed_id": payload.cv_id}


@router.post("/search-offres")
def search_offres(payload: CVSearchOffresRequest):
    """
    À partir d'un CV JSON, retourne les Top-N offres (collection offres).
    """
    result = search_offres_for_cv(payload.cv_json, top_k=payload.top_k)
    return result
