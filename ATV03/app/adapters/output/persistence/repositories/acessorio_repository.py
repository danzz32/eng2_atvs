from app.domain.models.acessorio import Acessorio
from sqlalchemy.orm import Session
from typing import List, Optional


class AcessorioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, acessorio: Acessorio) -> Acessorio:
        self.db.add(acessorio)
        self.db.commit()
        self.db.refresh(acessorio)
        return acessorio

    def get_all(self) -> list[type[Acessorio]]:
        return self.db.query(Acessorio).all()

    def get_by_id(self, id: int) -> Optional[Acessorio]:
        return self.db.query(Acessorio).filter(id == Acessorio.id).first()

    def update(self, acessorio: Acessorio) -> Acessorio:
        self.db.commit()
        self.db.refresh(acessorio)
        return acessorio

    def delete(self, acessorio: Acessorio) -> None:
        self.db.delete(acessorio)
        self.db.commit()
