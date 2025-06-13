class PartidaService:
    def __init__(self, partida_repository, estadio_disponibilidade_service):
        self.partida_repository = partida_repository
        self.estadio_disponibilidade_service = estadio_disponibilidade_service

    def cadastrar_partida(self, partida):
        if not self.estadio_disponibilidade_service.estadio_disponivel(partida.estadio.nome, partida.data):
            return False
        self.partida_repository.save(partida)
        return True
