import unittest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.output.persistence.database import Base
from app.adapters.output.persistence.repositories.locacao_repository import LocacaoRepository
from app.adapters.output.persistence.repositories.cliente_repository import ClienteRepository
from app.adapters.output.persistence.repositories.item_locacao_repository import ItemLocacaoRepository
from app.adapters.output.persistence.repositories.jogo_plataforma_repository import JogoPlataformaRepository
from app.adapters.output.persistence.repositories.jogo_repository import JogoRepository
from app.adapters.output.persistence.repositories.plataforma_repository import PlataformaRepository

from app.domain.models.cliente import Cliente
from app.domain.models.jogo import Jogo
from app.domain.models.plataforma import Plataforma
from app.domain.models.jogo_plataforma import JogoPlataforma
from app.domain.models.locacao import Locacao

from app.domain.services.locacao_service import LocacaoService


class TestLocacaoService(unittest.TestCase):

    def setUp(self):
        # Banco em memória
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Repositórios
        self.locacao_repo = LocacaoRepository(self.session)
        self.cliente_repo = ClienteRepository(self.session)
        self.item_locacao_repo = ItemLocacaoRepository(self.session)
        self.jogo_repo = JogoRepository(self.session)
        self.plataforma_repo = PlataformaRepository(self.session)
        self.jogo_plataforma_repo = JogoPlataformaRepository(self.session)

        # Serviço
        self.service = LocacaoService(
            self.locacao_repo,
            self.cliente_repo,
            self.item_locacao_repo,
            self.jogo_plataforma_repo,
            self.plataforma_repo,
            self.jogo_repo
        )

        # Cliente
        self.cliente = Cliente(nome="Fulano", email="fulano@email.com", senha="1234")
        self.cliente_repo.create(self.cliente)

        # Jogo e Plataformas
        self.jogo = Jogo(titulo="Elden Ring")
        self.jogo_repo.create(self.jogo)

        self.plataforma1 = Plataforma(nome="PS5")
        self.plataforma2 = Plataforma(nome="Xbox")
        self.plataforma_repo.create(self.plataforma1)
        self.plataforma_repo.create(self.plataforma2)

        # Jogo disponível em duas plataformas com preços diferentes
        self.jogo_plat1 = JogoPlataforma(jogo_id=self.jogo.id, plataforma_id=self.plataforma1.id, preco_diario=12.0)
        self.jogo_plat2 = JogoPlataforma(jogo_id=self.jogo.id, plataforma_id=self.plataforma2.id, preco_diario=15.0)
        self.jogo_plataforma_repo.create(self.jogo_plat1)
        self.jogo_plataforma_repo.create(self.jogo_plat2)

    def test_criar_locacao_e_adicionar_um_jogo(self):
        locacao = self.service.criar_locacao(self.cliente.id)
        item = self.service.adicionar_jogo_a_locacao(
            locacao_id=locacao.id,
            jogo_id=self.jogo.id,
            plataforma_id=self.plataforma1.id,
            quantidade=1,
            dias=3
        )
        self.assertIsNotNone(item.id)
        self.assertEqual(item.dias, 3)

    def test_adicionar_jogos_mesmo_jogo_em_plataformas_diferentes(self):
        locacao = self.service.criar_locacao(self.cliente.id)
        self.service.adicionar_jogo_a_locacao(locacao.id, self.jogo.id, self.plataforma1.id, quantidade=1, dias=2)
        self.service.adicionar_jogo_a_locacao(locacao.id, self.jogo.id, self.plataforma2.id, quantidade=1, dias=4)
        locacao_db = self.locacao_repo.get_by_id(locacao.id)
        self.assertEqual(len(locacao_db.itens), 2)

    def test_calcular_custo_total_da_locacao(self):
        locacao = self.service.criar_locacao(self.cliente.id)
        self.service.adicionar_jogo_a_locacao(locacao.id, self.jogo.id, self.plataforma1.id, quantidade=1, dias=3)
        self.service.adicionar_jogo_a_locacao(locacao.id, self.jogo.id, self.plataforma2.id, quantidade=1, dias=2)

        custo = self.service.calcular_custo_total(locacao.id)
        # 12 * 5 + 15 * 5 = 135.0
        self.assertAlmostEqual(custo, 66.0)


if __name__ == '__main__':
    unittest.main()
