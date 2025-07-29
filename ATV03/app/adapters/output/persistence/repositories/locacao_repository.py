from app.domain.models import Locacao
from app.domain.models.locacao import Locacao
from sqlalchemy.orm import Session
from typing import List, Optional


class LocacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, locacao: Locacao) -> Locacao:
        self.db.add(locacao)
        self.db.commit()
        self.db.refresh(locacao)
        return locacao

    def get_all(self) -> list[type[Locacao]]:
        return self.db.query(Locacao).all()

    def get_by_id(self, id: int) -> Optional[Locacao]:
        return self.db.query(Locacao).filter(id == Locacao.id).first()

    def update(self, locacao: Locacao) -> Locacao:
        self.db.commit()
        self.db.refresh(locacao)
        return locacao

    def delete(self, locacao: Locacao) -> None:
        self.db.delete(locacao)
        self.db.commit()
