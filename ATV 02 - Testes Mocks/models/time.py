from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from db.connection import Base

time_campeonato = Table(
    'time_campeonato',
    Base.metadata,
    Column('time_id', Integer, ForeignKey('times.id')),
    Column('campeonato_id', Integer, ForeignKey('campeonatos.id'))
)


class Time(Base):
    __tablename__ = 'times'

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)


    jogadores = relationship(
        "Jogador",
        back_populates="time",
        cascade="all, delete-orphan"
    )

    sede_id = Column(Integer, ForeignKey('estadios.id'))
    sede = relationship("Estadio", back_populates="time", uselist=False)

    partidasComoMandante = relationship(
        "Partida",
        back_populates="timeMandante",
        foreign_keys='Partida.timeMandante_id'
    )

    partidasComoVisitante = relationship(
        "Partida",
        back_populates="timeVisitante",
        foreign_keys='Partida.timeVisitante_id'
    )

    campeonatos = relationship(
        "Campeonato",
        secondary=time_campeonato,
        back_populates="times"
    )
