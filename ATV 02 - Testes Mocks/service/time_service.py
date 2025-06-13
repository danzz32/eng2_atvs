class TimeService:
    def __init__(self, time_repo, jogador_repo, notification_service):
        self.time_repo = time_repo
        self.jogador_repo = jogador_repo
        self.notification_service = notification_service

    def adicionar_jogador_ao_time(self, jogador_id, time_id):
        jogador = self.jogador_repo.get_by_id(jogador_id)
        time = self.time_repo.get_by_id(time_id)

        jogador.time = time  # associa o jogador ao time
        self.jogador_repo.save(jogador)  # salva o jogador atualizado

        self.notification_service.enviar_boas_vindas(jogador)
