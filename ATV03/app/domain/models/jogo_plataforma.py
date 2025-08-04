from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from app.adapters.output.persistence.database import Base


class JogoPlataforma(Base):
    __tablename__ = "jogos_plataformas"

    id = Column(Integer, primary_key=True, index=True)
    jogo_id = Column(Integer, ForeignKey("jogos.id"), nullable=False)
    plataforma_id = Column(Integer, ForeignKey("plataformas.id"), nullable=False)
    preco_diario = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('jogo_id', 'plataforma_id', name='uq_jogo_plataforma'),
    )

    jogo = relationship("Jogo", back_populates="jogos_plataformas")
    plataforma = relationship("Plataforma", back_populates="jogos_plataformas")
