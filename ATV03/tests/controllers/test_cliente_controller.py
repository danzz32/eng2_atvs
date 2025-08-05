import unittest
from fastapi.testclient import TestClient

# Importa o FastAPI app já configurado com as rotas
from app.adapters.input.http.main import app

client = TestClient(app)


class TestClienteRoutes(unittest.TestCase):

    def test_create_cliente(self):
        response = client.post("/clientes/",
                               json={"nome": "João Silva", "email": "joao.silva3@example.com", "senha": "123"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["nome"], "João Silva")

    def test_get_all_clientes(self):
        response = client.get("/clientes/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_cliente_by_id(self):
        # Primeiro cria um cliente para garantir existência
        response_create = client.post("/clientes/",
                                      json={"nome": "Carlos Lima", "email": "carlos.lima@example.com", "senha": "123"})
        cliente_id = response_create.json()["id"]

        response = client.get(f"/clientes/{cliente_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nome"], "Carlos Lima")

    def test_update_cliente(self):
        response_create = client.post("/clientes/",
                                      json={"nome": "Ana Souza", "email": "ana.souza@example.com", "senha": "123"})
        cliente_id = response_create.json()["id"]

        response = client.put(f"/clientes/{cliente_id}",
                              json={"nome": "Ana Paula", "email": "ana.paula@example.com", "senha": "123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["nome"], "Ana Paula")

    def test_delete_cliente(self):
        response_create = client.post("/clientes/", json={"nome": "Lucas Mendes", "email": "lucas.mendes@example.com",
                                                          "senha": "123"})
        cliente_id = response_create.json()["id"]

        response_delete = client.delete(f"/clientes/{cliente_id}")
        self.assertEqual(response_delete.status_code, 204)

        response_get = client.get(f"/clientes/{cliente_id}")
        self.assertEqual(response_get.status_code, 404)


if __name__ == '__main__':
    unittest.main()
