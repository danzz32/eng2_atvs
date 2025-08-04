from pydantic import BaseModel


class JogoPlataformaBase(BaseModel):
    preco_diario: float


class JogoPlataformaCreate(JogoPlataformaBase):
    jogo_id: int
    plataforma_id: int


class JogoPlataformaOut(JogoPlataformaBase):
    id: int
    jogo_id: int
    plataforma_id: int

    class Config:
        orm_mode = True
