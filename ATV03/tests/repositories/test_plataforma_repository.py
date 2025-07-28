import unittest
from app.adapters.output.persistence.repositories.plataforma_repository import PlataformaRepository
from app.domain.models.plataforma import Plataforma
from app.adapters.output.persistence.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestPlataformaRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.repo = PlataformaRepository(self.session)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_add_and_get(self):
        plataforma = Plataforma(nome="PS5")
        self.repo.create(plataforma)
        self.session.commit()

        result = self.repo.get_by_id(plataforma.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.nome, "PS5")

    def test_get_all(self):
        self.repo.create(Plataforma(nome="Xbox"))
        self.repo.create(Plataforma(nome="Switch"))
        self.session.commit()

        plataformas = self.repo.get_all()
        self.assertGreaterEqual(len(plataformas), 2)

    def test_delete(self):
        plataforma = Plataforma(nome="DeletePlataforma")
        self.repo.create(plataforma)
        self.session.commit()

        self.repo.delete(plataforma)
        self.session.commit()

        self.assertIsNone(self.repo.get_by_id(plataforma.id))


if __name__ == '__main__':
    unittest.main()
