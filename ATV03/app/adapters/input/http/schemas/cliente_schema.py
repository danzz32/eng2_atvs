from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None = None


class ClienteCreate(ClienteBase):
    senha: str


class ClienteOut(ClienteBase):
    id: int

    class Config:
        orm_mode = True
