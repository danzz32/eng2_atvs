from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.adapters.output.persistence.database import Base

# Tabela associativa para m .. n
acessorios_consoles = Table(
    "acessorios_consoles",
    Base.metadata,
    Column("acessorio_id", Integer, ForeignKey("acessorios.id")),
    Column("console_id", Integer, ForeignKey("consoles.id"))
)


class Acessorio(Base):
    __tablename__ = "acessorios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)

    consoles = relationship("Console", secondary=acessorios_consoles, back_populates="acessorios")
