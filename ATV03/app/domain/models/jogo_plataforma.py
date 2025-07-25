from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.adapters.output.persistence.database import Base


class JogoPlataforma(Base):
    __tablename__ = "jogos_plataformas"

    id = Column(Integer, primary_key=True, index=True)
    jogo_id = Column(Integer, ForeignKey("jogos.id"), nullable=False)
    plataforma_id = Column(Integer, ForeignKey("plataformas.id"), nullable=False)
    preco_diario = Column(Float, nullable=False)

    jogo = relationship("Jogo")
    plataforma = relationship("Plataforma")
