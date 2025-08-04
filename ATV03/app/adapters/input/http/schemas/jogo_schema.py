from pydantic import BaseModel
from typing import List, Optional
from .jogo_plataforma_schema import JogoPlataformaOut


class JogoBase(BaseModel):
    titulo: str


class JogoCreate(JogoBase):
    pass


class JogoOut(JogoBase):
    id: int
    jogos_plataformas: Optional[List[JogoPlataformaOut]] = []

    class Config:
        orm_mode = True
