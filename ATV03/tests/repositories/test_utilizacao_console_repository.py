import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.output.persistence.database import Base
from app.adapters.output.persistence.repositories.utilizacao_console_repository import UtilizacaoConsoleRepository
from app.adapters.output.persistence.repositories.cliente_repository import ClienteRepository
from app.adapters.output.persistence.repositories.console_repository import ConsoleRepository
from app.domain.models.utilizacao_console import UtilizacaoDoConsolePeloCliente
from app.domain.models.console import Console
from app.domain.models.cliente import Cliente
from datetime import datetime, timedelta


class TestUtilizacaoConsoleRepository(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.repo = UtilizacaoConsoleRepository(self.session)
        self.repo_cliente = ClienteRepository(self.session)
        self.repo_console = ConsoleRepository(self.session)

        # Cria cliente e console
        self.cliente = Cliente(nome="João", email="joao@email.com", senha="1234")
        self.repo_cliente.create(self.cliente)

        self.console = Console(nome="PlayStation 5", preco_por_hora=10.0)
        self.repo_console.create(self.console)

        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_add(self):
        uso = UtilizacaoDoConsolePeloCliente(
            cliente_id=self.cliente.id,
            console_id=self.console.id,
            inicio=datetime.now(),
            fim=datetime.now() + timedelta(hours=2.5)
        )
        self.repo.create(uso)
        self.session.commit()

        found = self.repo.get_by_id(uso.id)
        self.assertIsNotNone(found)

    def test_get_by_id(self):
        uso = UtilizacaoDoConsolePeloCliente(
            cliente_id=self.cliente.id,
            console_id=self.console.id,
            inicio=datetime.now(),
            fim=datetime.now() + timedelta(hours=2.5)
        )
        self.repo.create(uso)
        self.session.commit()

        found = self.repo.get_by_id(uso.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.cliente_id, self.cliente.id)
        self.assertEqual(found.console_id, self.console.id)


if __name__ == '__main__':
    unittest.main()
