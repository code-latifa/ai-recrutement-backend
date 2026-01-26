from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class OffreEmploi(Base):
    __tablename__ = "offres_emploi"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # UUID
    recruteur_id: Mapped[str] = mapped_column(String(255), ForeignKey("recruteurs.id"), nullable=False)
    titre: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    lieu: Mapped[str] = mapped_column(String(255), nullable=False)
    type_contrat: Mapped[str] = mapped_column(String(50), nullable=False)  # CDI, CDD, Stage, etc.
    salaire_min: Mapped[float] = mapped_column(nullable=True)
    salaire_max: Mapped[float] = mapped_column(nullable=True)
    competences_requises: Mapped[str] = mapped_column(String(1000), nullable=True)  # JSON array en string
    experience_requise: Mapped[str] = mapped_column(String(100), nullable=True)  # junior, confirmé, senior
    niveau_etude: Mapped[str] = mapped_column(String(100), nullable=True)
    secteur: Mapped[str] = mapped_column(String(255), nullable=True)
    date_creation: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification: Mapped[object] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    date_expiration: Mapped[object] = mapped_column(DateTime(timezone=True), nullable=False)
    statut: Mapped[str] = mapped_column(String(50), nullable=False, default="active")  # active, fermée, archivée
