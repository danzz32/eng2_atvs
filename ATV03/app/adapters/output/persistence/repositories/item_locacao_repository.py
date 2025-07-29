from app.domain.models.item_locacao import ItemLocacao
from sqlalchemy.orm import Session
from typing import List, Optional, Any


class ItemLocacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item: ItemLocacao) -> ItemLocacao:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_all(self) -> list[type[ItemLocacao]]:
        return self.db.query(ItemLocacao).all()

    def get_by_id(self, id: int) -> Optional[ItemLocacao]:
        return self.db.query(ItemLocacao).filter(id == ItemLocacao.id).first()

    def get_by_locacao(self, locacao_id: int) -> list[type[ItemLocacao]]:
        return self.db.query(ItemLocacao).filter(locacao_id == ItemLocacao.locacao_id).all()

    def update(self, item: ItemLocacao) -> ItemLocacao:
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: ItemLocacao) -> None:
        self.db.delete(item)
        self.db.commit()
