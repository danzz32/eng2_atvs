from pydantic import BaseModel


class AcessorioBase(BaseModel):
    nome: str


class AcessorioCreate(AcessorioBase):
    pass


class AcessorioOut(AcessorioBase):
    id: int

    class Config:
        orm_mode = True
