import random

class EstatisticaService:
    def get_estatisticas(self, jogador_id: int) -> dict:
        """
        Simula o retorno de estatísticas para o jogador.
        Retorna um dicionário com dados fictícios.
        """
        # Simulando valores aleatórios para gols e assistências
        estatisticas = {
            "gols": random.randint(0, 30),
            "assistencias": random.randint(0, 20),
            "partidas_jogadas": random.randint(0, 38)
        }
        return estatisticas
