import pytest
from service.campeonato_service import CampeonatoService, CampeonatoIniciadoException


def test_quando_campeonato_ja_iniciado_entao_nao_adiciona_time_e_lanca_excecao(mocker):
    # Arrange
    campeonato_mock = mocker.Mock()
    campeonato_mock.iniciado = True
    campeonato_mock.times = []

    campeonato_repo_mock = mocker.Mock()
    campeonato_repo_mock.get_by_id.return_value = campeonato_mock

    service = CampeonatoService(campeonato_repo_mock)
    time_mock = mocker.Mock()

    # Act + Assert
    with pytest.raises(CampeonatoIniciadoException) as excinfo:
        service.adicionar_time(campeonato_id=1, time=time_mock)

    assert "já foi iniciado" in str(excinfo.value)
    campeonato_repo_mock.update.assert_not_called()


def test_quando_campeonato_nao_iniciado_entao_adiciona_time_e_salva_alteracao(mocker):
    # Arrange
    campeonato_mock = mocker.Mock()
    campeonato_mock.iniciado = False
    campeonato_mock.times = []

    campeonato_repo_mock = mocker.Mock()
    campeonato_repo_mock.get_by_id.return_value = campeonato_mock
    campeonato_repo_mock.update.return_value = campeonato_mock

    service = CampeonatoService(campeonato_repo_mock)
    time_mock = mocker.Mock()

    # Act
    service.adicionar_time(campeonato_id=1, time=time_mock)

    # Assert
    assert time_mock in campeonato_mock.times
    campeonato_repo_mock.update.assert_called_once_with(campeonato_mock)
