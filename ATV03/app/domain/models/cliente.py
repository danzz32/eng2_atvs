from sqlalchemy import Column, Integer, String

from app.adapters.output.persistence.database import Base

# entidade
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefone = Column(String)
    senha = Column(String, nullable=False)
