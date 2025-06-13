from sqlalchemy.orm import Session
from models.estadio import Estadio


class EstadioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Estadio).all()

    def get_by_id(self, estadio_id: int):
        return self.db.query(Estadio).filter(Estadio.id == estadio_id).first()

    def create(self, estadio: Estadio):
        self.db.add(estadio)
        self.db.commit()
        self.db.refresh(estadio)
        return estadio

    def delete(self, estadio_id: int):
        estadio = self.get_by_id(estadio_id)
        if estadio:
            self.db.delete(estadio)
            self.db.commit()
            return True
        return False
