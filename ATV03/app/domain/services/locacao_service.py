from datetime import datetime

from app.domain.models import ItemLocacao
from app.domain.models.locacao import Locacao
from app.adapters.output.persistence.repositories.locacao_repository import LocacaoRepository
from app.adapters.output.persistence.repositories.cliente_repository import ClienteRepository
from app.adapters.output.persistence.repositories.item_locacao_repository import ItemLocacaoRepository
from app.adapters.output.persistence.repositories.jogo_plataforma_repository import JogoPlataformaRepository
from app.adapters.output.persistence.repositories.jogo_repository import JogoRepository
from app.adapters.output.persistence.repositories.plataforma_repository import PlataformaRepository


class LocacaoService:
    def __init__(self, locacao_repository: LocacaoRepository, cliente_repository: ClienteRepository,
                 item_locacao_repository: ItemLocacaoRepository, jogo_plataforma_repository: JogoPlataformaRepository,
                 plataforma_repository: PlataformaRepository, jogo_repository: JogoRepository):
        self.locacao_repository = locacao_repository
        self.cliente_repository = cliente_repository
        self.item_locacao_repository = item_locacao_repository
        self.jogo_plataforma_repository = jogo_plataforma_repository
        self.jogo_repository = jogo_repository
        self.plataforma_repository = plataforma_repository

    def criar_locacao(self, cliente_id: int) -> Locacao:
        cliente = self.cliente_repository.get_by_id(cliente_id)
        if not cliente:
            raise ValueError(f"Cliente com ID {cliente_id} não encontrado.")

        nova_locacao = Locacao(cliente_id=cliente_id, data=datetime.now())
        self.locacao_repository.create(nova_locacao)
        return nova_locacao

    def adicionar_jogo_a_locacao(self, locacao_id: int, jogo_id: int, plataforma_id: int, quantidade: int,
                                 dias: int) -> ItemLocacao:
        locacao = self.locacao_repository.get_by_id(locacao_id)
        if not locacao:
            raise ValueError("Locação não encontrada.")

        jogo = self.jogo_repository.get_by_id(jogo_id)
        if not jogo:
            raise ValueError("Jogo não encontrado.")

        plataforma = self.plataforma_repository.get_by_id(plataforma_id)
        if not plataforma:
            raise ValueError("Plataforma não encontrada.")

        jogo_plataforma = self.jogo_plataforma_repository.get_game_platform(jogo_id, plataforma_id)
        if not jogo_plataforma:
            raise ValueError("O jogo não está disponível para a plataforma informada.")

        item_locacao = ItemLocacao(
            dias=dias,
            quantidade=quantidade,
            jogo_plataforma_id=jogo_plataforma.id,
            locacao_id=locacao_id
        )

        self.item_locacao_repository.create(item_locacao)
        return item_locacao

    def calcular_custo_total(self, locacao_id: int) -> float:
        locacao = self.locacao_repository.get_by_id(locacao_id)
        if not locacao:
            raise ValueError("Locação não encontrada.")

        if not locacao.itens:
            return 0.0

        custo_total = 0.0
        for item in locacao.itens:
            jogo_plataforma = self.jogo_plataforma_repository.get_by_id(item.jogo_plataforma_id)
            if not jogo_plataforma:
                raise ValueError(f"Preço não encontrado para o item de locação {item.id}.")

            custo_item = jogo_plataforma.preco_diario * item.dias * item.quantidade
            custo_total += custo_item

        return custo_total
