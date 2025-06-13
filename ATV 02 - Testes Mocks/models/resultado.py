from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.connection import Base

class Resultado(Base):
    __tablename__ = 'resultados'

    id = Column(Integer, primary_key=True)
    numGolsMandante = Column(Integer)
    numGolsVisitante = Column(Integer)

    partida_id = Column(Integer, ForeignKey("partidas.id"))
    partida = relationship("Partida", back_populates="resultado")

    def getPontuacaoMandante(self):
        if self.numGolsMandante > self.numGolsVisitante:
            return 3
        elif self.numGolsMandante == self.numGolsVisitante:
            return 1
        return 0

    def getPontuacaoVisitante(self):
        if self.numGolsVisitante > self.numGolsMandante:
            return 3
        elif self.numGolsVisitante == self.numGolsMandante:
            return 1
        return 0

    def jogoSaiuEmpatado(self):
        return self.numGolsMandante == self.numGolsVisitante
