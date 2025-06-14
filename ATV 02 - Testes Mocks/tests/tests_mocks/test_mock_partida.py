import pytest
from datetime import date
from models.partida import Partida
from models.estadio import Estadio
from service.partida_service import PartidaService


@pytest.fixture
def estadio_mock():
    estadio = Estadio()
    estadio.nome = "Estádio Nacional"
    return estadio


@pytest.fixture
def partida(estadio_mock):
    return Partida(data=date(2025, 6, 15), estadio=estadio_mock)


def test_cadastrar_partida_quando_estadio_disponivel_entao_salva_partida(mocker, partida, estadio_mock):
    mock_repo = mocker.Mock()
    mock_disponibilidade_service = mocker.Mock()
    mock_disponibilidade_service.estadio_disponivel.return_value = True

    service = PartidaService(mock_repo, mock_disponibilidade_service)

    resultado = service.cadastrar_partida(partida)

    mock_disponibilidade_service.estadio_disponivel.assert_called_once_with(
        estadio_mock.nome, partida.data
    )
    mock_repo.save.assert_called_once_with(partida)  # <- Corrigido aqui
    assert resultado is True
