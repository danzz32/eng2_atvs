from app.domain.models.plataforma import Plataforma
from sqlalchemy.orm import Session
from typing import List, Optional


class PlataformaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, plataforma: Plataforma) -> Plataforma:
        self.db.add(plataforma)
        self.db.commit()
        self.db.refresh(plataforma)
        return plataforma

    def get_all(self) -> List[Plataforma]:
        return self.db.query(Plataforma).all()

    def get_by_id(self, id: int) -> Optional[Plataforma]:
        return self.db.query(Plataforma).filter(Plataforma.id == id).first()

    def update(self, plataforma: Plataforma) -> Plataforma:
        self.db.commit()
        self.db.refresh(plataforma)
        return plataforma

    def delete(self, plataforma: Plataforma) -> None:
        self.db.delete(plataforma)
        self.db.commit()
