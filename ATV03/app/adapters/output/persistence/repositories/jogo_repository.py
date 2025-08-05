from app.domain.models import Jogo
from app.domain.models.jogo import Jogo
from sqlalchemy.orm import Session
from typing import List, Optional, Type


class JogoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, jogo: Jogo) -> Jogo:
        self.db.add(jogo)
        self.db.commit()
        self.db.refresh(jogo)
        return jogo

    def get_all(self) -> list[Type[Jogo]]:
        return self.db.query(Jogo).all()

    def get_by_id(self, id: int) -> Optional[Jogo]:
        return self.db.query(Jogo).filter(Jogo.id == id).first()

    def update(self, jogo_id: int, dados: dict):
        jogo = self.get_by_id(jogo_id)
        if not jogo:
            return None
        for key, value in dados.items():
            setattr(jogo, key, value)
        self.db.commit()
        self.db.refresh(jogo)
        return jogo

    def delete(self, jogo: Jogo) -> None:
        self.db.delete(jogo)
        self.db.commit()
