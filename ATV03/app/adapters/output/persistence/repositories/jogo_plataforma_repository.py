from app.domain.models.jogo_plataforma import JogoPlataforma
from sqlalchemy.orm import Session
from typing import List, Optional


class JogoPlataformaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, relacao: JogoPlataforma) -> JogoPlataforma:
        self.db.add(relacao)
        self.db.commit()
        self.db.refresh(relacao)
        return relacao

    def get_all(self) -> List[JogoPlataforma]:
        return self.db.query(JogoPlataforma).all()

    def get_by_id(self, id: int) -> Optional[JogoPlataforma]:
        return self.db.query(JogoPlataforma).filter(JogoPlataforma.id == id).first()

    def update(self, relacao: JogoPlataforma) -> JogoPlataforma:
        self.db.commit()
        self.db.refresh(relacao)
        return relacao

    def delete(self, relacao: JogoPlataforma) -> None:
        self.db.delete(relacao)
        self.db.commit()
