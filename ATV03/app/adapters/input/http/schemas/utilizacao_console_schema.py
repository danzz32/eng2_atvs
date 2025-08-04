from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UtilizacaoConsoleBase(BaseModel):
    inicio: Optional[datetime] = None
    fim: Optional[datetime] = None
    console_id: int
    cliente_id: int


class UtilizacaoConsoleCreate(UtilizacaoConsoleBase):
    pass


class UtilizacaoConsoleOut(UtilizacaoConsoleBase):
    id: int

    class Config:
        orm_mode = True
