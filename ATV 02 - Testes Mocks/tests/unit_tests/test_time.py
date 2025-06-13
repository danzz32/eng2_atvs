import datetime
from models.time import Time
from models.jogador import Jogador
from repository.time_repository import TimeRepository
import pytest
from sqlalchemy.exc import IntegrityError


def test_persistir_time_com_jogadores(db_session):
    time_repo = TimeRepository(db_session)

    # Criar lista de jogadores (ainda não salvos)
    jogadores = [
        Jogador(nome="João", nascimento=datetime.date(1990, 1, 1), genero="M", altura=180),
        Jogador(nome="Maria", nascimento=datetime.date(1992, 5, 10), genero="F", altura=165),
    ]

    # Criar time com jogadores associados
    time = Time(nome="Time da Galera", jogadores=jogadores)

    # Persistir no banco
    time_repo.create(time)

    # Buscar novamente pelo ID
    time_salvo = time_repo.get_by_id(time.id)

    # Asserções
    assert time_salvo is not None
    assert time_salvo.nome == "Time da Galera"
    assert len(time_salvo.jogadores) == 2

    nomes = [j.nome for j in time_salvo.jogadores]
    assert "João" in nomes
    assert "Maria" in nomes

    # Impressão para depuração
    print('\n')
    for jogador in time_salvo.jogadores:
        print(f"Jogador: id={jogador.id}, nome={jogador.nome}, time_id={jogador.time_id}")


def test_nao_permitir_time_com_nome_duplicado(db_session):
    time_repo = TimeRepository(db_session)

    # Primeiro time
    time1 = Time(nome="Duplicado FC")
    time_repo.create(time1)

    # Segundo time com o mesmo nome
    time2 = Time(nome="Duplicado FC")

    with pytest.raises(IntegrityError) as exc_info:
        time_repo.create(time2)

    # Recupera a sessão após erro
    db_session.rollback()

    # Verificação final: só 1 time com esse nome deve existir
    times = db_session.query(Time).filter_by(nome="Duplicado FC").all()
    assert len(times) == 1

    # Impressão para depuração
    print('\n')
    print(f"Time persistido: id={times[0].id}, nome={times[0].nome}")
