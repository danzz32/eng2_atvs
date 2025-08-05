from datetime import datetime
from app.domain.models.utilizacao_console import UtilizacaoDoConsolePeloCliente
from app.adapters.output.persistence.repositories.utilizacao_console_repository import UtilizacaoConsoleRepository
from app.adapters.output.persistence.repositories.console_repository import ConsoleRepository


class UtilizacaoConsoleService:
    def __init__(self, utilizacao_repo: UtilizacaoConsoleRepository, console_repo: ConsoleRepository):
        self.utilizacao_repo = utilizacao_repo
        self.console_repo = console_repo

    def iniciar_utilizacao(self, cliente_id: int, console_id: int) -> UtilizacaoDoConsolePeloCliente:
        console = self.console_repo.get_by_id(console_id)
        if not console:
            raise ValueError(f"Console com id {console_id} não encontrado")

        uso = UtilizacaoDoConsolePeloCliente(
            cliente_id=cliente_id,
            console_id=console_id,
            inicio=datetime.now(),
            fim=None
        )
        return self.utilizacao_repo.create(uso)

    def finalizar_utilizacao(self, utilizacao_id: int) -> float:
        uso = self.utilizacao_repo.get_by_id(utilizacao_id)
        if not uso:
            raise ValueError(f"Utilização com id {utilizacao_id} não encontrada")

        if uso.fim is not None:
            raise ValueError("Utilização já finalizada")

        uso.fim = datetime.utcnow()
        self.utilizacao_repo.update(uso)

        duracao = uso.fim - uso.inicio
        horas = duracao.total_seconds() / 3600

        console = self.console_repo.get_by_id(uso.console_id)
        if not console:
            raise ValueError("Console associado não encontrado")

        custo_total = horas * console.preco_por_hora
        return custo_total
