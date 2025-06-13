from sqlalchemy.orm import Session
from models.partida import Partida
from models.estadio import Estadio
from datetime import date


class PartidaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Partida).all()

    def get_by_id(self, partida_id: int):
        return self.db.query(Partida).filter(Partida.id == partida_id).first()

    def get_by_date(self, data: date):
        return self.db.query(Partida).filter(Partida.data == data).all()

    def get_by_estadio(self, estadio_id: int):
        return self.db.query(Partida).filter_by(estadio_id=estadio_id).all()

    def get_by_estadio_nome(self, nome_estadio: str):
        return (
            self.db.query(Partida)
            .join(Partida.estadio)
            .filter(Estadio.nome == nome_estadio)
            .all()
        )

    def create(self, partida: Partida):
        self.db.add(partida)
        self.db.commit()
        self.db.refresh(partida)
        return partida

    def delete(self, partida_id: int):
        partida = self.get_by_id(partida_id)
        if partida:
            self.db.delete(partida)
            self.db.commit()
            return True
        return False
