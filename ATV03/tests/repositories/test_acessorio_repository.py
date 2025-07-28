import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.output.persistence.database import Base
from app.adapters.output.persistence.repositories.acessorio_repository import AcessorioRepository
from app.adapters.output.persistence.repositories.console_repository import ConsoleRepository
from app.domain.models.acessorio import Acessorio
from app.domain.models.console import Console


class TestAcessorioRepository(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.repo = AcessorioRepository(self.session)

    def test_add(self):
        acessorio = Acessorio(nome="Controle Extra")
        self.repo.create(acessorio)

    def test_get_by_id(self):
        acessorio = Acessorio(nome="Controle Extra")
        self.repo.create(acessorio)
        acessorio_recuperado = self.repo.get_by_id(acessorio.id)
        self.assertIsNotNone(acessorio_recuperado)


if __name__ == '__main__':
    unittest.main()
