from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.utils.logger import setup_logging

# Routers (certains peuvent être encore vides)
from app.api.auth import router as auth_router
# from app.api.candidats import router as candidats_router
# from app.api.recruteurs import router as recruteurs_router
# from app.api.offres import router as offres_router
# from app.api.candidatures import router as candidatures_router
# from app.api.matching import router as matching_router
# from app.api.notification import router as notifications_router

# -------------------------------------------------
# Setup logging
# -------------------------------------------------
setup_logging()

# -------------------------------------------------
# Create FastAPI app
# -------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI-powered recruitment platform API"
)

# -------------------------------------------------
# CORS configuration
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Health check
# -------------------------------------------------
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

# -------------------------------------------------
# API Routers
# -------------------------------------------------
app.include_router(auth_router)
#app.include_router(candidats_router)
#app.include_router(recruteurs_router)
#app.include_router(offres_router)
#app.include_router(candidatures_router)
#app.include_router(matching_router)
#app.include_router(notifications_router)
