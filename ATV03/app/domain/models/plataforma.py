from sqlalchemy import Column, Integer, String

from app.adapters.output.persistence.database import Base


class Plataforma(Base):
    __tablename__ = "plataformas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
