from pydantic import BaseModel
from typing import List, Optional
from .jogo_plataforma_schema import JogoPlataformaOut


class PlataformaBase(BaseModel):
    nome: str


class PlataformaCreate(PlataformaBase):
    pass


class PlataformaOut(PlataformaBase):
    id: int
    jogos_plataformas: Optional[List[JogoPlataformaOut]] = []

    class Config:
        orm_mode = True
