import pytest
from unittest.mock import Mock
from datetime import date

# Importa as classes reais (ajuste o caminho conforme seu projeto)
from models.time import Time
from models.partida import Partida
from models.resultado import Resultado
from service.classificacao_service import ClassificacaoService  # supondo onde está a service


@pytest.fixture
def times_mock():
    # Cria dois times simulados
    time1 = Mock(spec=Time)
    time1.id = 1
    time1.nome = "Time A"

    time2 = Mock(spec=Time)
    time2.id = 2
    time2.nome = "Time B"

    return [time1, time2]


@pytest.fixture
def partidas_mock(times_mock):
    time1, time2 = times_mock

    resultado1 = Mock(spec=Resultado)
    resultado1.getPontuacaoMandante.return_value = 3  # Vitória do mandante (time1)
    resultado1.getPontuacaoVisitante.return_value = 0
    resultado1.jogoSaiuEmpatado.return_value = False

    partida1 = Mock(spec=Partida)
    partida1.timeMandante = time1
    partida1.timeVisitante = time2
    partida1.resultado = resultado1
    partida1.data = date(2025, 6, 1)

    resultado2 = Mock(spec=Resultado)
    resultado2.getPontuacaoMandante.return_value = 1  # Empate
    resultado2.getPontuacaoVisitante.return_value = 1
    resultado2.jogoSaiuEmpatado.return_value = True

    partida2 = Mock(spec=Partida)
    partida2.timeMandante = time2
    partida2.timeVisitante = time1
    partida2.resultado = resultado2
    partida2.data = date(2025, 6, 8)

    return [partida1, partida2]


def test_calcular_classificacao(times_mock, partidas_mock):
    # Mocks dos repositórios
    mock_time_repo = Mock()
    mock_partida_repo = Mock()

    mock_time_repo.get_all.return_value = times_mock
    mock_partida_repo.get_all.return_value = partidas_mock

    service = ClassificacaoService(mock_partida_repo, mock_time_repo)
    classificacao = service.calcular_classificacao()

    # Verifica chamadas dos repositórios
    mock_time_repo.get_all.assert_called_once()
    mock_partida_repo.get_all.assert_called_once()

    # time1: 3 pontos (vitoria) + 1 ponto (empate) = 4 pontos
    # time2: 0 pontos (derrota) + 1 ponto (empate) = 1 ponto

    # Verifica ordem
    assert classificacao[0]['time'].id == 1
    assert classificacao[0]['pontos'] == 4
    assert classificacao[1]['time'].id == 2
    assert classificacao[1]['pontos'] == 1

    # Verifica jogos, vitórias, empates e derrotas
    assert classificacao[0]['jogos'] == 2
    assert classificacao[0]['vitorias'] == 1
    assert classificacao[0]['empates'] == 1
    assert classificacao[0]['derrotas'] == 0

    assert classificacao[1]['jogos'] == 2
    assert classificacao[1]['vitorias'] == 0
    assert classificacao[1]['empates'] == 1
    assert classificacao[1]['derrotas'] == 1
