import pytest
from models.jogador import Jogador
from models.time import Time
from service.jogador_service import JogadorService
from service.estatistica_service import EstatisticaService
from service.time_service import TimeService
from datetime import date

def test_salvar_jogador_sem_nome_nao_chama_save(mocker):
    mock_repo = mocker.Mock()

    # Instancia serviço com repositório mockado
    service = JogadorService(mock_repo)

    # Jogador sem nome
    jogador_sem_nome = Jogador(nome="", nascimento=date(2000, 1, 1), genero=None, altura=None)

    # Chama o metodo do serviço
    resultado = service.salvar_jogador(jogador_sem_nome)

    # Verifica que save NÃO foi chamado
    mock_repo.save.assert_not_called()

    # Verifica que retornou False (ou comportamento esperado)
    assert resultado is False

def test_servico_estatisticas_retorna_dados_e_persiste_jogador(mocker):
    # Mocks
    mock_repo = mocker.Mock()
    mock_estatistica_service = mocker.Mock(spec=EstatisticaService)

    # Simula retorno da API de estatísticas
    estatisticas_mock = {
        "gols": 7,
        "assistencias": 3,
        "partidas_jogadas": 15
    }
    mock_estatistica_service.get_estatisticas.return_value = estatisticas_mock

    # Cria jogador e o salva com o JogadorService (sem lógica de estatísticas)
    jogador = Jogador(nome="Maria", nascimento=date(1999, 5, 10), genero="F", altura=170)
    jogador.id = 1

    service = JogadorService(mock_repo)
    resultado = service.salvar_jogador(jogador)

    # Após salvar, simula atualização com estatísticas
    estatisticas = mock_estatistica_service.get_estatisticas(jogador.id)
    jogador.gols = estatisticas["gols"]
    jogador.assistencias = estatisticas["assistencias"]
    jogador.partidas_jogadas = estatisticas["partidas_jogadas"]

    # Persiste jogador atualizado
    mock_repo.save(jogador)

    # Verificações
    assert resultado is True
    mock_estatistica_service.get_estatisticas.assert_called_once_with(1)
    mock_repo.save.assert_called_with(jogador)
    assert jogador.gols == 7
    assert jogador.assistencias == 3
    assert jogador.partidas_jogadas == 15



def test_adicionar_jogador_envia_notificacao(mocker):
    # Mocks
    mock_time_repo = mocker.Mock()
    mock_jogador_repo = mocker.Mock()
    mock_notification_service = mocker.Mock()

    # Criar objetos simulados
    jogador_mock = Jogador(id=1, nome="Ronaldo", nascimento=date(1985, 2, 5))
    time_mock = Time(id=10, nome="Time Azul")

    # Configura retorno dos métodos get_by_id
    mock_jogador_repo.get_by_id.return_value = jogador_mock
    mock_time_repo.get_by_id.return_value = time_mock

    # Instanciar serviço com mocks
    service = TimeService(mock_time_repo, mock_jogador_repo, mock_notification_service)

    # Ação: adicionar jogador ao time
    service.adicionar_jogador_ao_time(jogador_id=1, time_id=10)

    # O jogador deve ter a referência para o time atualizada
    assert jogador_mock.time == time_mock

    # O repositório de jogadores deve salvar o jogador atualizado (ou o de times, dependendo da implementação)
    mock_jogador_repo.save.assert_called_once_with(jogador_mock)

    # O serviço de notificação deve ter sido chamado com o jogador correto
    mock_notification_service.enviar_boas_vindas.assert_called_once_with(jogador_mock)