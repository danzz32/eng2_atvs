class CampeonatoIniciadoException(Exception):
    pass


class CampeonatoService:
    def __init__(self, campeonato_repo):
        self.campeonato_repo = campeonato_repo

    def adicionar_time(self, campeonato_id: int, time):
        campeonato = self.campeonato_repo.get_by_id(campeonato_id)
        if not campeonato:
            raise ValueError("Campeonato não encontrado")

        # Supondo que o Campeonato tenha um atributo booleano 'iniciado'
        if getattr(campeonato, 'iniciado', False):
            raise CampeonatoIniciadoException("Campeonato já foi iniciado")

        # Adiciona o time
        campeonato.times.append(time)
        self.campeonato_repo.update(campeonato)
