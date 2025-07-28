from sqlalchemy import Column, Integer, String

from app.adapters.output.persistence.database import Base


class Jogo(Base):
    __tablename__ = "jogos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
