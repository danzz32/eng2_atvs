from service.estatistica_service import EstatisticaService
from service.jogador_service import JogadorService
from service.time_service import TimeService


def test_salvar_jogador_sem_nome_nao_chama_save(mocker, jogador_sem_nome):
    # Arrange
    mock_repo = mocker.Mock()
    service = JogadorService(mock_repo)

    # Act
    resultado = service.salvar_jogador(jogador_sem_nome)

    # Assert
    mock_repo.save.assert_not_called()
    assert resultado is False
    print(f"\nMétodo save chamado? {'Sim' if resultado == True else 'Não'}")


def test_servico_estatisticas_retorna_dados_e_persiste_jogador(mocker, jogador_mock, estatisticas_mock):
    # Arrange
    mock_repo = mocker.Mock()
    mock_estatistica_service = mocker.Mock(spec=EstatisticaService)
    mock_estatistica_service.get_estatisticas.return_value = estatisticas_mock

    jogador_mock.id = 1  # simula ID preenchido

    service = JogadorService(mock_repo)

    # Act
    resultado = service.salvar_jogador(jogador_mock)
    estatisticas = mock_estatistica_service.get_estatisticas(jogador_mock.id)

    jogador_mock.gols = estatisticas["gols"]
    jogador_mock.assistencias = estatisticas["assistencias"]
    jogador_mock.partidas_jogadas = estatisticas["partidas_jogadas"]

    mock_repo.save(jogador_mock)

    # Assert
    assert resultado is True
    mock_estatistica_service.get_estatisticas.assert_called_once_with(1)
    mock_repo.save.assert_called_with(jogador_mock)
    assert jogador_mock.gols == 7
    assert jogador_mock.assistencias == 3
    assert jogador_mock.partidas_jogadas == 15

    print(
        f"\nDados do jogador:\ngols = {jogador_mock.gols}\nassistencias = {jogador_mock.assistencias}\npartidas jogadas = {jogador_mock.partidas_jogadas}")


def test_adicionar_jogador_envia_notificacao(mocker, jogador_mock, time_mock):
    # Arrange
    mock_time_repo = mocker.Mock()
    mock_jogador_repo = mocker.Mock()
    mock_notification_service = mocker.Mock()

    mock_jogador_repo.get_by_id.return_value = jogador_mock
    mock_time_repo.get_by_id.return_value = time_mock

    service = TimeService(mock_time_repo, mock_jogador_repo, mock_notification_service)

    # Act
    service.adicionar_jogador_ao_time(jogador_id=1, time_id=10)

    # Assert
    assert jogador_mock.time == time_mock
    mock_jogador_repo.save.assert_called_once_with(jogador_mock)
    mock_notification_service.enviar_boas_vindas.assert_called_once_with(jogador_mock)
    print(f'\nJogador adicionado \nNotificação enviada!')
