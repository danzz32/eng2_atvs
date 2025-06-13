import random


class EstadioDisponibilidadeService:
    def estadio_disponivel(self, estadio: str, data) -> bool:
        """
        Simula verificação de disponibilidade de um estádio.
        """
        disp = random.randint(0, 1)
        if disp == 1:
            return True
        return False
