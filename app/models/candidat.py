from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base

class Candidat(Base):
    __tablename__ = "candidats"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # UUID
    user_id: Mapped[str] = mapped_column(String(255), ForeignKey("utilisateurs.id"), nullable=False)
    prenom: Mapped[str] = mapped_column(String(100), nullable=False)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    telephone: Mapped[str] = mapped_column(String(20), nullable=True)
    adresse: Mapped[str] = mapped_column(String(500), nullable=True)
    ville: Mapped[str] = mapped_column(String(100), nullable=True)
    code_postal: Mapped[str] = mapped_column(String(10), nullable=True)
    niveau_experience: Mapped[str] = mapped_column(String(50), nullable=True)  # junior, confirmé, senior, etc.
    specialites: Mapped[str] = mapped_column(String(500), nullable=True)  # JSON array en string
    date_inscription: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification: Mapped[object] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
