from pydantic import BaseModel
from typing import List
from .acessorio_schema import AcessorioOut


class ConsoleBase(BaseModel):
    nome: str
    preco_por_hora: float


class ConsoleCreate(ConsoleBase):
    acessorios_ids: list[int] = []  # IDs para associar acessórios


class ConsoleOut(ConsoleBase):
    id: int
    acessorios: List[AcessorioOut] = []

    class Config:
        orm_mode = True
