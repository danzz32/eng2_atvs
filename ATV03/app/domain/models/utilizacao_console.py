from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.adapters.output.persistence.database import Base
# entidade 

class UtilizacaoDoConsolePeloCliente(Base):
    __tablename__ = "utilizacoes_console"

    id = Column(Integer, primary_key=True, index=True)
    inicio = Column(DateTime, default=datetime.now)
    fim = Column(DateTime, nullable=True)

    console_id = Column(Integer, ForeignKey("consoles.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    console = relationship("Console")
    cliente = relationship("Cliente")
