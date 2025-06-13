from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.connection import Base


class Estadio(Base):
    __tablename__ = 'estadios'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    endereco = Column(String)

    time = relationship("Time", back_populates="sede", uselist=False)
    partidas = relationship("Partida", back_populates="estadio")  # ADICIONE ESTA LINHA
