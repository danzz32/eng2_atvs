from app.domain.models import UtilizacaoDoConsolePeloCliente
from app.domain.models.utilizacao_console import UtilizacaoDoConsolePeloCliente
from sqlalchemy.orm import Session
from typing import List, Optional


class UtilizacaoConsoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, uso: UtilizacaoDoConsolePeloCliente) -> UtilizacaoDoConsolePeloCliente:
        self.db.add(uso)
        self.db.commit()
        self.db.refresh(uso)
        return uso

    def get_all(self) -> list[type[UtilizacaoDoConsolePeloCliente]]:
        return self.db.query(UtilizacaoDoConsolePeloCliente).all()

    def get_by_id(self, id: int) -> Optional[UtilizacaoDoConsolePeloCliente]:
        return self.db.query(UtilizacaoDoConsolePeloCliente).filter(UtilizacaoDoConsolePeloCliente.id == id).first()

    def update(self, uso: UtilizacaoDoConsolePeloCliente) -> UtilizacaoDoConsolePeloCliente:
        self.db.commit()
        self.db.refresh(uso)
        return uso

    def delete(self, uso: UtilizacaoDoConsolePeloCliente) -> None:
        self.db.delete(uso)
        self.db.commit()
