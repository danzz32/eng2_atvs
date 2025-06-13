from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.connection import Base
from models.time import time_campeonato

class Campeonato(Base):
    __tablename__ = 'campeonatos'

    id = Column(Integer, primary_key=True)
    ano = Column(Integer)
    nome = Column(String, nullable=False)

    partidas = relationship("Partida", back_populates="campeonato")
    times = relationship("Time", secondary=time_campeonato, back_populates="campeonatos")
