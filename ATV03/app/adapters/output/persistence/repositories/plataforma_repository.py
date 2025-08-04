from app.domain.models import Plataforma
from app.domain.models.plataforma import Plataforma
from sqlalchemy.orm import Session
from typing import List, Optional, Type


class PlataformaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, plataforma: Plataforma) -> Plataforma:
        self.db.add(plataforma)
        self.db.commit()
        self.db.refresh(plataforma)
        return plataforma

    def get_all(self) -> list[Type[Plataforma]]:
        return self.db.query(Plataforma).all()

    def get_by_id(self, id: int) -> Optional[Plataforma]:
        return self.db.query(Plataforma).filter(id == Plataforma.id).first()

    def get_by_name(self, name: str) -> Optional[Plataforma]:
        return self.db.query(Plataforma).filter(name == Plataforma.nome).first()

    def update(self, plataforma: Plataforma) -> Plataforma:
        self.db.commit()
        self.db.refresh(plataforma)
        return plataforma

    def delete(self, plataforma: Plataforma) -> None:
        self.db.delete(plataforma)
        self.db.commit()
