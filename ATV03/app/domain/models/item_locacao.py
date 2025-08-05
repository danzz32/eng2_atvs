from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.adapters.output.persistence.database import Base
from app.domain.models.jogo_plataforma import JogoPlataforma


# entidade
class ItemLocacao(Base):
    __tablename__ = "itens_locacao"

    id = Column(Integer, primary_key=True, index=True)
    dias = Column(Integer, nullable=False)
    quantidade = Column(Integer, nullable=False)

    jogo_plataforma_id = Column(Integer, ForeignKey("jogos_plataformas.id"), nullable=False)
    locacao_id = Column(Integer, ForeignKey("locacoes.id"), nullable=False)

    jogo_plataforma = relationship(JogoPlataforma)
    locacao = relationship("Locacao", back_populates="itens")
