from sqlalchemy import Column, Integer, String
from app.adapters.output.persistence.database import Base
from sqlalchemy.orm import relationship

# entidade
class Plataforma(Base):
    __tablename__ = "plataformas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    jogos_plataformas = relationship("JogoPlataforma", back_populates="plataforma")
