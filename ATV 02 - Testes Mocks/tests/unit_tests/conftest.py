import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.connection import Base

# Importa todas as models para registrar as tabelas no metadata
import models.jogador
import models.time
import models.campeonato
import models.partida
import models.estadio
import models.resultado

# Engine de testes em memória
engine_test = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine_test)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
        Base.metadata.drop_all(bind=engine_test)
