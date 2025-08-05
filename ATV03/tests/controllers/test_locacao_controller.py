import unittest
from fastapi.testclient import TestClient
from app.adapters.input.http.main import app
from app.adapters.output.persistence import database
from app.domain.models.cliente import Cliente
from app.domain.models.locacao import Locacao
import uuid

client = TestClient(app)


class TestLocacaoRoutes(unittest.TestCase):

    def setUp(self):
        # Cria cliente para testes, com email único para evitar conflito
        email_unico = f"teste_{uuid.uuid4()}@example.com"
        response = client.post("/clientes/", json={
            "nome": "Cliente Teste",
            "email": email_unico,
            "senha": "123"
        })
        self.assertEqual(response.status_code, 201)
        self.cliente_id = response.json()["id"]

    def tearDown(self):
        # Limpa locações e clientes criados nos testes para não interferir em outros testes
        db = next(database.get_db())
        try:
            db.query(Locacao).delete()
            db.query(Cliente).delete()
            db.commit()
        finally:
            db.close()

    def test_create_locacao_cliente_inexistente(self):
        response = client.post("/locacoes/", json={"cliente_id": 999999})
        self.assertEqual(response.status_code, 404)

    def test_create_locacao(self):
        response = client.post("/locacoes/", json={"cliente_id": self.cliente_id})

        # DEBUG: para ajudar a ver o que está acontecendo
        print("\nResponse status:", response.status_code)
        print("Response body:", response.json())

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["cliente_id"], self.cliente_id)

    def test_get_all_locacoes(self):
        # Garante que exista pelo menos uma locação
        client.post("/locacoes/", json={"cliente_id": self.cliente_id})

        response = client.get("/locacoes/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_locacao_by_id(self):
        response_create = client.post("/locacoes/", json={"cliente_id": self.cliente_id})
        locacao_id = response_create.json()["id"]

        response = client.get(f"/locacoes/{locacao_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["cliente_id"], self.cliente_id)

    def test_update_locacao(self):
        response_create = client.post("/locacoes/", json={"cliente_id": self.cliente_id})
        locacao_id = response_create.json()["id"]

        from datetime import datetime
        nova_data = datetime.now().isoformat()

        response = client.put(f"/locacoes/{locacao_id}", json={"cliente_id": self.cliente_id, "data": nova_data})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["cliente_id"], self.cliente_id)
        self.assertIn("data", response.json())

    def test_delete_locacao(self):
        response_create = client.post("/locacoes/", json={"cliente_id": self.cliente_id})
        locacao_id = response_create.json()["id"]

        response_delete = client.delete(f"/locacoes/{locacao_id}")
        self.assertEqual(response_delete.status_code, 204)

        response_get = client.get(f"/locacoes/{locacao_id}")
        self.assertEqual(response_get.status_code, 404)


if __name__ == '__main__':
    unittest.main()
