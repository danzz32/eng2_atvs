from app.domain.models.item_locacao import ItemLocacao
from sqlalchemy.orm import Session
from typing import List, Optional


class ItemLocacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item: ItemLocacao) -> ItemLocacao:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_all(self) -> List[ItemLocacao]:
        return self.db.query(ItemLocacao).all()

    def get_by_id(self, id: int) -> Optional[ItemLocacao]:
        return self.db.query(ItemLocacao).filter(ItemLocacao.id == id).first()

    def update(self, item: ItemLocacao) -> ItemLocacao:
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: ItemLocacao) -> None:
        self.db.delete(item)
        self.db.commit()
