import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from db.connection import Base

# Importa todas as models para registrar as tabelas no metadata
import models.jogador
import models.time
import models.campeonato
import models.partida
import models.estadio
import models.resultado

from models.jogador import Jogador
from models.time import Time

# Engine de testes em memória
engine_test = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


# ============================
# Fixture para banco de dados
# ============================
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


# ===============================
# Fixtures para objetos de modelo
# ===============================

@pytest.fixture
def jogador_mock():
    return Jogador(id=1, nome="Ronaldo", nascimento=date(1985, 2, 5))


@pytest.fixture
def time_mock():
    return Time(id=10, nome="Time Azul")


@pytest.fixture
def jogador_sem_nome():
    return Jogador(nome="", nascimento=date(2000, 1, 1))


@pytest.fixture
def estatisticas_mock():
    return {
        "gols": 7,
        "assistencias": 3,
        "partidas_jogadas": 15
    }
