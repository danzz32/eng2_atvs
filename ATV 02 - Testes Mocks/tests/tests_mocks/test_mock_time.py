import pytest
from service.campeonato_service import CampeonatoService, CampeonatoIniciadoException

def test_adicionar_time_campeonato_iniciado(mocker):
    # Mock do campeonato com 'iniciado' = True e lista times
    campeonato_mock = mocker.Mock()
    campeonato_mock.iniciado = True
    campeonato_mock.times = []

    # Mock do repositorio
    campeonato_repo_mock = mocker.Mock()
    campeonato_repo_mock.get_by_id.return_value = campeonato_mock

    service = CampeonatoService(campeonato_repo_mock)
    time_mock = mocker.Mock()

    with pytest.raises(CampeonatoIniciadoException) as excinfo:
        service.adicionar_time(campeonato_id=1, time=time_mock)

    assert "já foi iniciado" in str(excinfo.value)
    campeonato_repo_mock.update.assert_not_called()

def test_adicionar_time_campeonato_nao_iniciado(mocker):
    campeonato_mock = mocker.Mock()
    campeonato_mock.iniciado = False
    campeonato_mock.times = []

    campeonato_repo_mock = mocker.Mock()
    campeonato_repo_mock.get_by_id.return_value = campeonato_mock
    campeonato_repo_mock.update.return_value = campeonato_mock

    service = CampeonatoService(campeonato_repo_mock)
    time_mock = mocker.Mock()

    service.adicionar_time(campeonato_id=1, time=time_mock)

    assert time_mock in campeonato_mock.times
    campeonato_repo_mock.update.assert_called_once_with(campeonato_mock)
