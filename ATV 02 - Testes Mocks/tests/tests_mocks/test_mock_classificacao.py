import pytest
from service.classificacao_service import ClassificacaoService
from unittest.mock import Mock
from datetime import date


@pytest.fixture
def times_mock():
    time1 = Mock(id=1, nome="Time A")
    time2 = Mock(id=2, nome="Time B")
    return [time1, time2]


@pytest.fixture
def partidas_mock(times_mock):
    time1, time2 = times_mock

    resultado1 = Mock()
    resultado1.getPontuacaoMandante.return_value = 3
    resultado1.getPontuacaoVisitante.return_value = 0
    resultado1.jogoSaiuEmpatado.return_value = False

    partida1 = Mock()
    partida1.timeMandante = time1
    partida1.timeVisitante = time2
    partida1.resultado = resultado1
    partida1.data = date(2025, 6, 1)

    resultado2 = Mock()
    resultado2.getPontuacaoMandante.return_value = 1
    resultado2.getPontuacaoVisitante.return_value = 1
    resultado2.jogoSaiuEmpatado.return_value = True

    partida2 = Mock()
    partida2.timeMandante = time2
    partida2.timeVisitante = time1
    partida2.resultado = resultado2
    partida2.data = date(2025, 6, 8)

    return [partida1, partida2]


def test_calcular_classificacao(mocker, times_mock, partidas_mock):
    # Arrange
    mock_time_repo = mocker.Mock()
    mock_partida_repo = mocker.Mock()

    mock_time_repo.get_all.return_value = times_mock
    mock_partida_repo.get_all.return_value = partidas_mock

    service = ClassificacaoService(mock_partida_repo, mock_time_repo)

    # Act
    classificacao = service.calcular_classificacao()

    # Assert: chamadas aos repositórios
    mock_time_repo.get_all.assert_called_once()
    mock_partida_repo.get_all.assert_called_once()

    # Verifica ordenação da classificação
    assert classificacao[0]['time'].id == 1  # Time A
    assert classificacao[0]['pontos'] == 4
    assert classificacao[1]['time'].id == 2  # Time B
    assert classificacao[1]['pontos'] == 1

    # Verifica estatísticas do Time A
    assert classificacao[0]['jogos'] == 2
    assert classificacao[0]['vitorias'] == 1
    assert classificacao[0]['empates'] == 1
    assert classificacao[0]['derrotas'] == 0

    # Verifica estatísticas do Time B
    assert classificacao[1]['jogos'] == 2
    assert classificacao[1]['vitorias'] == 0
    assert classificacao[1]['empates'] == 1
    assert classificacao[1]['derrotas'] == 1
