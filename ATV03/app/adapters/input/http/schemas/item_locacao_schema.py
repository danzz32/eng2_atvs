from pydantic import BaseModel


class ItemLocacaoBase(BaseModel):
    dias: int
    quantidade: int
    jogo_plataforma_id: int


class ItemLocacaoCreate(ItemLocacaoBase):
    locacao_id: int


class ItemLocacaoOut(ItemLocacaoBase):
    id: int
    locacao_id: int

    class Config:
        orm_mode = True
