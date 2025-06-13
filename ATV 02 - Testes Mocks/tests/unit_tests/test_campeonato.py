import datetime
import pytest
from models.campeonato import Campeonato
from models.time import Time
from models.partida import Partida
from models.resultado import Resultado
from repository.time_repository import TimeRepository
from repository.campeonato_repository import CampeonatoRepository
from repository.resultado_repository import ResultadoRepository
from repository.partida_repository import PartidaRepository


def test_atualizar_classificacao_apos_resultados(db_session):
    # Instanciar os repositórios envolvidos
    time_repo = TimeRepository(db_session)
    partida_repo = PartidaRepository(db_session)
    resultado_repo = ResultadoRepository(db_session)
    campeonato_repo = CampeonatoRepository(db_session)

    # Criar campeonato
    campeonato = Campeonato(nome="Campeonato Teste")
    campeonato_repo.create(campeonato)

    # Criar times
    time1 = Time(nome="Time A")
    time2 = Time(nome="Time B")
    time_repo.create(time1)
    time_repo.create(time2)

    # Associar times ao campeonato
    campeonato.times.append(time1)
    campeonato.times.append(time2)
    campeonato_repo.update(campeonato)

    # Criar partidas entre os times dentro do campeonato
    partida1 = Partida(data=datetime.date(2025, 6, 1), timeMandante=time1, timeVisitante=time2, campeonato=campeonato)
    partida_repo.create(partida1)

    # Criar resultado para a partida
    resultado1 = Resultado(numGolsMandante=2, numGolsVisitante=1, partida=partida1)
    resultado_repo.create(resultado1)

    # Atualizar classificação (supondo metodo que recalcula pontos da tabela)
    campeonato_repo.atualizar_classificacao(campeonato.id)

    # Buscar times para verificar a pontuação atualizada (supondo atributo 'pontos' ou similar)
    times_atualizados = campeonato_repo.get_times_por_campeonato(campeonato.id)

    # Verificar se time1 (vencedor) recebeu 3 pontos
    time1_atual = next(t for t in times_atualizados if t.id == time1.id)
    assert time1_atual.pontos == 3

    # Verificar se time2 recebeu 0 pontos
    time2_atual = next(t for t in times_atualizados if t.id == time2.id)
    assert time2_atual.pontos == 0
