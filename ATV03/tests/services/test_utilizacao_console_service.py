import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

from app.domain.models.utilizacao_console import UtilizacaoDoConsolePeloCliente
from app.domain.models.console import Console
from app.adapters.output.persistence.repositories.utilizacao_console_repository import UtilizacaoConsoleRepository
from app.adapters.output.persistence.repositories.console_repository import ConsoleRepository
from app.domain.services.utilizacao_console_service import UtilizacaoConsoleService


class TestConsoleService(unittest.TestCase):

    def setUp(self):
        self.mock_utilizacao_repo = MagicMock(spec=UtilizacaoConsoleRepository)
        self.mock_console_repo = MagicMock(spec=ConsoleRepository)

        self.service = UtilizacaoConsoleService(
            utilizacao_repo=self.mock_utilizacao_repo,
            console_repo=self.mock_console_repo
        )

        # Dados básicos para os testes
        self.cliente_id = 1
        self.console_id = 10
        self.utilizacao_id = 100

    def test_iniciar_utilizacao_sucesso(self):
        # Mock do console retornado
        console = Console(id=self.console_id, nome="Console X", preco_por_hora=10.0)
        self.mock_console_repo.get_by_id.return_value = console

        # Mock da criação da utilização
        uso = UtilizacaoDoConsolePeloCliente(
            id=self.utilizacao_id,
            cliente_id=self.cliente_id,
            console_id=self.console_id,
            inicio=datetime.now(),
            fim=None
        )
        self.mock_utilizacao_repo.create.return_value = uso

        resultado = self.service.iniciar_utilizacao(self.cliente_id, self.console_id)

        self.mock_console_repo.get_by_id.assert_called_once_with(self.console_id)
        self.mock_utilizacao_repo.create.assert_called_once()
        self.assertEqual(resultado, uso)

    def test_iniciar_utilizacao_console_inexistente(self):
        self.mock_console_repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as context:
            self.service.iniciar_utilizacao(self.cliente_id, self.console_id)
        self.assertIn("Console com id", str(context.exception))

    def test_finalizar_utilizacao_sucesso(self):
        inicio = datetime.now() - timedelta(hours=2)
        fim = None
        uso = UtilizacaoDoConsolePeloCliente(
            id=self.utilizacao_id,
            cliente_id=self.cliente_id,
            console_id=self.console_id,
            inicio=inicio,
            fim=fim
        )
        console = Console(id=self.console_id, nome="Console X", preco_por_hora=15.0)

        self.mock_utilizacao_repo.get_by_id.return_value = uso
        self.mock_console_repo.get_by_id.return_value = console

        # Mock do update
        self.mock_utilizacao_repo.update.return_value = uso

        custo = self.service.finalizar_utilizacao(self.utilizacao_id)

        self.mock_utilizacao_repo.get_by_id.assert_called_once_with(self.utilizacao_id)
        self.mock_console_repo.get_by_id.assert_called_once_with(self.console_id)
        self.mock_utilizacao_repo.update.assert_called_once_with(uso)

        esperado = 2 * 15.0  # 2 horas * preço por hora
        self.assertAlmostEqual(custo, esperado, places=2)

    def test_finalizar_utilizacao_inexistente(self):
        self.mock_utilizacao_repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as context:
            self.service.finalizar_utilizacao(self.utilizacao_id)
        self.assertIn("Utilização com id", str(context.exception))

    def test_finalizar_utilizacao_ja_finalizada(self):
        uso = UtilizacaoDoConsolePeloCliente(
            id=self.utilizacao_id,
            cliente_id=self.cliente_id,
            console_id=self.console_id,
            inicio=datetime.now() - timedelta(hours=1),
            fim=datetime.now()
        )
        self.mock_utilizacao_repo.get_by_id.return_value = uso

        with self.assertRaises(ValueError) as context:
            self.service.finalizar_utilizacao(self.utilizacao_id)
        self.assertIn("Utilização já finalizada", str(context.exception))

    def test_finalizar_utilizacao_console_inexistente(self):
        uso = UtilizacaoDoConsolePeloCliente(
            id=self.utilizacao_id,
            cliente_id=self.cliente_id,
            console_id=self.console_id,
            inicio=datetime.now() - timedelta(hours=1),
            fim=None
        )
        self.mock_utilizacao_repo.get_by_id.return_value = uso
        self.mock_console_repo.get_by_id.return_value = None

        with self.assertRaises(ValueError) as context:
            self.service.finalizar_utilizacao(self.utilizacao_id)
        self.assertIn("Console associado não encontrado", str(context.exception))


if __name__ == "__main__":
    unittest.main()
