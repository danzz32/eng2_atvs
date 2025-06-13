from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.connection import Base

class Jogador(Base):
    __tablename__ = 'jogadores'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    nascimento = Column(Date)
    genero = Column(String)
    altura = Column(Integer)

    time_id = Column(Integer, ForeignKey('times.id'))
    time = relationship("Time", back_populates="jogadores")
