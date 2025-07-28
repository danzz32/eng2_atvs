import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.output.persistence.database import Base
from app.adapters.output.persistence.repositories.console_repository import ConsoleRepository
from app.domain.models.console import Console


class TestConsoleRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.repo = ConsoleRepository(self.session)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_add_and_get(self):
        console = Console(nome="PS4 Slim", preco_por_hora=15.0)
        self.repo.create(console)
        self.session.commit()

        result = self.repo.get_by_id(console.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.nome, "PS4 Slim")

    def test_get_all(self):
        self.repo.create(Console(nome="Xbox One", preco_por_hora=15.0))
        self.repo.create(Console(nome="Switch OLED", preco_por_hora=15.0))
        self.session.commit()

        consoles = self.repo.get_all()
        self.assertGreaterEqual(len(consoles), 2)

    def test_delete(self):
        console = Console(nome="DeleteConsole",preco_por_hora=15.0)
        self.repo.create(console)
        self.session.commit()

        self.repo.delete(console)
        self.session.commit()

        self.assertIsNone(self.repo.get_by_id(console.id))


if __name__ == '__main__':
    unittest.main()
