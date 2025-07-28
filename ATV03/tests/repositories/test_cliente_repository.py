import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.output.persistence.database import Base
from app.domain.models.cliente import Cliente
from app.adapters.output.persistence.repositories.cliente_repository import ClienteRepository


class TestClienteRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.repo = ClienteRepository(self.session)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_create_and_get(self):
        cliente = Cliente(nome="João", email="joao@example.com", senha="1234")
        self.repo.create(cliente)
        result = self.repo.get_by_id(cliente.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.nome, "João")

    def test_update(self):
        cliente = Cliente(nome="Maria", email="maria@example.com", senha="1234")
        self.repo.create(cliente)

        updated_data = {"nome": "Maria Silva", "email": "maria.silva@example.com"}
        updated_cliente = self.repo.update(cliente.id, updated_data)

        self.assertIsNotNone(updated_cliente)
        self.assertEqual(updated_cliente.nome, "Maria Silva")
        self.assertEqual(updated_cliente.email, "maria.silva@example.com")

        cliente_db = self.repo.get_by_id(cliente.id)
        self.assertEqual(cliente_db.nome, "Maria Silva")
        self.assertEqual(cliente_db.email, "maria.silva@example.com")

    def test_delete(self):
        cliente = Cliente(nome="Carlos", email="carlos@example.com", senha="1234")
        self.repo.create(cliente)
        self.repo.delete(cliente)
        result = self.repo.get_by_id(cliente.id)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
