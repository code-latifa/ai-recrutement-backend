from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class Recruteur(Base):
    __tablename__ = "recruteurs"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # UUID
    user_id: Mapped[str] = mapped_column(String(255), ForeignKey("utilisateurs.id"), nullable=False)
    nom_entreprise: Mapped[str] = mapped_column(String(255), nullable=False)
    poste: Mapped[str] = mapped_column(String(255), nullable=False)
    telephone: Mapped[str] = mapped_column(String(20), nullable=True)
    adresse: Mapped[str] = mapped_column(String(500), nullable=True)
    date_inscription: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification: Mapped[object] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
