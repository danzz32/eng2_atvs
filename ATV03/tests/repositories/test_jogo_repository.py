import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.output.persistence.repositories.jogo_repository import JogoRepository
from app.adapters.output.persistence.database import Base
from app.domain.models.jogo import Jogo
from app.adapters.output.persistence.database import SessionLocal


class TestJogoRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.repo = JogoRepository(self.session)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_add_and_get(self):
        jogo = Jogo(titulo="Zelda")
        self.repo.create(jogo)
        self.session.commit()

        found = self.repo.get_by_id(jogo.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.titulo, "Zelda")

    def test_get_all(self):
        self.repo.create(Jogo(titulo="Halo"))
        self.repo.create(Jogo(titulo="FIFA"))
        self.session.commit()

        all_jogos = self.repo.get_all()
        self.assertGreaterEqual(len(all_jogos), 2)

    def test_delete(self):
        jogo = Jogo(titulo="DeleteMe")
        self.repo.create(jogo)
        self.session.commit()

        self.repo.delete(jogo)
        self.session.commit()

        self.assertIsNone(self.repo.get_by_id(jogo.id))


if __name__ == '__main__':
    unittest.main()
