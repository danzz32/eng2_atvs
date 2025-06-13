from sqlalchemy.orm import Session
from models.jogador import Jogador


class JogadorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Jogador).all()

    def get_by_id(self, jogador_id: int):
        return self.db.query(Jogador).filter(Jogador.id == jogador_id).first()

    def get_by_name(self, nome: str):
        return self.db.query(Jogador).filter(Jogador.nome.ilike(f"%{nome}%")).all()

    def create(self, jogador: Jogador):
        self.db.add(jogador)
        self.db.commit()
        self.db.refresh(jogador)
        return jogador

    def update(self, jogador):
        self.db.merge(jogador)
        self.db.commit()

    def delete(self, jogador_id: int):
        jogador = self.get_by_id(jogador_id)
        if jogador:
            self.db.delete(jogador)
            self.db.commit()
            return True
        return False
