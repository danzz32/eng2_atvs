import unittest
from fastapi.testclient import TestClient
from app.adapters.input.http.main import app
import uuid

client = TestClient(app)


class TestUtilizacaoConsoleRoutes(unittest.TestCase):

    def setUp(self):
        # Criar cliente
        cliente_resp = client.post("/clientes/", json={
            "nome": "Cliente Teste",
            "email": f"teste_{uuid.uuid4()}@example.com",
            "senha": "123"
        })
        assert cliente_resp.status_code == 201, f"Erro ao criar cliente: {cliente_resp.json()}"
        self.cliente_id = cliente_resp.json()["id"]

        # Criar console
        console_resp = client.post("/consoles/", json={
            "nome": "PlayStation 5",
            "preco_por_hora": 15.0
        })
        assert console_resp.status_code == 201, f"Erro ao criar console: {console_resp.json()}"
        self.console_id = console_resp.json()["id"]

    def test_iniciar_utilizacao(self):

        response = client.post("/utilizacoes/", json={
            "cliente_id": self.cliente_id,
            "console_id": self.console_id
        })

        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["cliente_id"], self.cliente_id)
        self.assertEqual(response.json()["console_id"], self.console_id)


    def test_finalizar_utilizacao(self):
        # Primeiro inicia a utilização
        response_iniciar = client.post("/utilizacoes/", json={
            "cliente_id": self.cliente_id,
            "console_id": self.console_id
        })
        uso_id = response_iniciar.json()["id"]

        # Depois finaliza
        response_finalizar = client.post(f"/utilizacoes/{uso_id}/finalizar")
        self.assertEqual(response_finalizar.status_code, 200)
        self.assertIsInstance(response_finalizar.json(), float)  # custo total

    def test_listar_utilizacoes(self):
        response = client.get("/utilizacoes/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_buscar_utilizacao_por_id(self):
        response_iniciar = client.post("/utilizacoes/", json={
            "cliente_id": self.cliente_id,
            "console_id": self.console_id
        })
        uso_id = response_iniciar.json()["id"]

        response = client.get(f"/utilizacoes/{uso_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], uso_id)

    def test_deletar_utilizacao(self):
        response_iniciar = client.post("/utilizacoes/", json={
            "cliente_id": self.cliente_id,
            "console_id": self.console_id
        })
        uso_id = response_iniciar.json()["id"]

        response_delete = client.delete(f"/utilizacoes/{uso_id}")
        self.assertEqual(response_delete.status_code, 204)

        response_get = client.get(f"/utilizacoes/{uso_id}")
        self.assertEqual(response_get.status_code, 404)


if __name__ == '__main__':
    unittest.main()
