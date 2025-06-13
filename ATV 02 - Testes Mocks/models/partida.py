from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.connection import Base


class Partida(Base):
    __tablename__ = 'partidas'

    id = Column(Integer, primary_key=True)
    data = Column(Date)

    timeMandante_id = Column(Integer, ForeignKey("times.id"))
    timeVisitante_id = Column(Integer, ForeignKey("times.id"))
    campeonato_id = Column(Integer, ForeignKey("campeonatos.id"))
    estadio_id = Column(Integer, ForeignKey("estadios.id"))  # ADICIONE ESTA LINHA

    timeMandante = relationship("Time", foreign_keys=[timeMandante_id], back_populates="partidasComoMandante")
    timeVisitante = relationship("Time", foreign_keys=[timeVisitante_id], back_populates="partidasComoVisitante")
    campeonato = relationship("Campeonato", back_populates="partidas")

    estadio = relationship("Estadio", back_populates="partidas")  # ADICIONE ESTA LINHA

    resultado = relationship("Resultado", uselist=False, back_populates="partida", cascade="all, delete")
