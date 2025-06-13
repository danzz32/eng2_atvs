import datetime
from models.partida import Partida
from models.campeonato import Campeonato
from models.estadio import Estadio
from repository.partida_repository import PartidaRepository
from repository.campeonato_repository import CampeonatoRepository


def test_busca_partida_por_data(db_session):
    campeonato_repo = CampeonatoRepository(db_session)
    campeonato = Campeonato(nome="Brasileirão", ano=2025)
    campeonato_repo.create(campeonato)

    partida_repo = PartidaRepository(db_session)

    # Criar partidas com datas diferentes
    partidas = [
        Partida(data=datetime.date(2025, 6, 1), campeonato_id=campeonato.id),
        Partida(data=datetime.date(2025, 6, 1), campeonato_id=campeonato.id),
        Partida(data=datetime.date(2025, 6, 2), campeonato_id=campeonato.id),
        Partida(data=datetime.date(2025, 6, 3), campeonato_id=campeonato.id),
    ]

    for partida in partidas:
        partida_repo.create(partida)

    # Busca partidas da data 2025-06-01
    resultados = partida_repo.get_by_date(datetime.date(2025, 6, 1))

    assert len(resultados) == 2
    for partida in resultados:
        assert partida.data == datetime.date(2025, 6, 1)

    # Imprime as partidas encontradas para conferência
    print('\n')
    for partida in resultados:
        print(f"Partida encontrada: id={partida.id}, data={partida.data}")


def test_buscar_partidas_por_estadio(db_session):
    repo = PartidaRepository(db_session)

    # Criar estádios
    estadio1 = Estadio(nome="Estádio Maracanã", endereco="RJ")
    estadio2 = Estadio(nome="Estádio Beira-Rio", endereco="RS")
    db_session.add_all([estadio1, estadio2])
    db_session.commit()

    # Criar partidas em diferentes estádios
    partida1 = Partida(data=datetime.date(2025, 6, 1), estadio=estadio1)
    partida2 = Partida(data=datetime.date(2025, 6, 2), estadio=estadio1)
    partida3 = Partida(data=datetime.date(2025, 6, 3), estadio=estadio2)
    db_session.add_all([partida1, partida2, partida3])
    db_session.commit()

    partidas_maracana = repo.get_by_estadio(estadio1.id)

    assert len(partidas_maracana) == 2
    assert all(p.estadio_id == estadio1.id for p in partidas_maracana)

    print('\n')
    print(f"Partidas no {estadio1.nome}: {[p.id for p in partidas_maracana]}")
