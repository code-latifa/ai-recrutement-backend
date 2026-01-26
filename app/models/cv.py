from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class CV(Base):
    __tablename__ = "cvs"

    id: Mapped[str] = mapped_column(String, primary_key=True)  # UUID
    candidat_id: Mapped[str] = mapped_column(String(255), ForeignKey("candidats.id"), nullable=False)
    nom_fichier: Mapped[str] = mapped_column(String(255), nullable=False)
    chemin_fichier: Mapped[str] = mapped_column(String(500), nullable=False)
    contenu_extraction: Mapped[str] = mapped_column(Text, nullable=True)  # JSON contenant infos extraites
    embedding_vector: Mapped[str] = mapped_column(Text, nullable=True)  # Embedding stocké en JSON
    competences: Mapped[str] = mapped_column(String(1000), nullable=True)  # JSON array
    experiences: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array
    formations: Mapped[str] = mapped_column(Text, nullable=True)  # JSON array
    langues: Mapped[str] = mapped_column(String(500), nullable=True)  # JSON array
    date_upload: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    date_modification: Mapped[object] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    version: Mapped[int] = mapped_column(nullable=False, default=1)
