from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.adapters.output.persistence.database import Base
from app.domain.models.cliente import Cliente
from app.domain.models.item_locacao import ItemLocacao
# entidade
class Locacao(Base):
    __tablename__ = "locacoes"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(DateTime, default=datetime.now())
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship(Cliente, backref="locacoes")
    itens = relationship(ItemLocacao, back_populates="locacao", cascade="all, delete-orphan")
