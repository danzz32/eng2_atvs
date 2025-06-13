# test_mock_partida.py
from datetime import date
from models.partida import Partida
from models.estadio import Estadio
from service.partida_service import PartidaService


def test_cadastrar_partida_chama_servico_disponibilidade(mocker):
    # Mocks
    mock_repo = mocker.Mock()
    mock_disponibilidade_service = mocker.Mock()

    # Estádio mockado com nome
    estadio_mock = Estadio()
    estadio_mock.nome = "Estádio Nacional"

    # Simula que o estádio está disponível
    mock_disponibilidade_service.estadio_disponivel.return_value = True

    # Instância do serviço
    service = PartidaService(mock_repo, mock_disponibilidade_service)

    # Criação da partida com estádio como objeto
    partida = Partida(data=date(2025, 6, 15), estadio=estadio_mock)

    # Ação
    resultado = service.cadastrar_partida(partida)

    # Verificação
    mock_disponibilidade_service.estadio_disponivel.assert_called_once_with(
        "Estádio Nacional", date(2025, 6, 15)
    )
    assert resultado is True
