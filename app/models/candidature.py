from sqlalchemy import String, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class Candidature(Base):
    __tablename__ = "candidatures"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # UUID
    candidat_id: Mapped[str] = mapped_column(String(255), ForeignKey("candidats.id"), nullable=False)
    offre_emploi_id: Mapped[str] = mapped_column(String(255), ForeignKey("offres_emploi.id"), nullable=False)
    cv_id: Mapped[str] = mapped_column(String(255), ForeignKey("cvs.id"), nullable=False)
    score_matching: Mapped[float] = mapped_column(Float, nullable=True)  # Score de compatibilité
    statut: Mapped[str] = mapped_column(String(50), nullable=False, default="en_attente")  # en_attente, acceptée, rejetée, entretien
    motif_rejet: Mapped[str] = mapped_column(String(500), nullable=True)
    feedback_ia: Mapped[str] = mapped_column(String(1000), nullable=True)  # Analyse IA du matching
    date_candidature: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification: Mapped[object] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    date_reponse: Mapped[object] = mapped_column(DateTime(timezone=True), nullable=True)
