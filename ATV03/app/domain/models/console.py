from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.adapters.output.persistence.database import Base
from app.domain.models.acessorio import acessorios_consoles

# entidade
class Console(Base):
    __tablename__ = "consoles"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco_por_hora = Column(Float, nullable=False)

    acessorios = relationship("Acessorio", secondary=acessorios_consoles, back_populates="consoles")
