from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ItemLocacaoOut(BaseModel):
    id: int

    # Aqui você pode colocar outros campos do ItemLocacao, ex:
    # jogo_id: int
    # quantidade: int

    class Config:
        orm_mode = True


class LocacaoCreate(BaseModel):
    cliente_id: int
    data: Optional[datetime] = None  # pode deixar para preencher automaticamente no banco
    # Você pode opcionalmente aceitar itens na criação, se desejar:
    # itens: Optional[List[ItemLocacaoCreate]] = []


class LocacaoOut(BaseModel):
    id: int
    data: datetime
    cliente_id: int
    itens: List[ItemLocacaoOut] = []

    class Config:
        orm_mode = True
