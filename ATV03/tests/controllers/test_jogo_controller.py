import unittest
from fastapi.testclient import TestClient

from app.adapters.input.http.main import app

client = TestClient(app)


class TestJogoRoutes(unittest.TestCase):

    def test_create_jogo(self):
        response = client.post("/jogos/", json={"titulo": "Super Mario"})
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["titulo"], "Super Mario")

    def test_get_all_jogos(self):
        response = client.get("/jogos/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_jogo_by_id(self):
        # Primeiro cria um jogo para garantir existência
        response_create = client.post("/jogos/", json={"titulo": "Zelda"})
        jogo_id = response_create.json()["id"]

        response = client.get(f"/jogos/{jogo_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["titulo"], "Zelda")

    def test_update_jogo(self):
        response_create = client.post("/jogos/", json={"titulo": "Old Title"})
        jogo_id = response_create.json()["id"]

        response = client.put(f"/jogos/{jogo_id}", json={"titulo": "New Title"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["titulo"], "New Title")

    def test_delete_jogo(self):
        response_create = client.post("/jogos/", json={"titulo": "To Delete"})
        jogo_id = response_create.json()["id"]

        response_delete = client.delete(f"/jogos/{jogo_id}")
        self.assertEqual(response_delete.status_code, 204)

        response_get = client.get(f"/jogos/{jogo_id}")
        self.assertEqual(response_get.status_code, 404)


if __name__ == '__main__':
    unittest.main()
