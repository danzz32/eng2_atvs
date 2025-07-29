from .jogo import Jogo
from .plataforma import Plataforma
from .jogo_plataforma import JogoPlataforma
from .cliente import Cliente
from .locacao import Locacao
from .item_locacao import ItemLocacao
from .utilizacao_console import UtilizacaoDoConsolePeloCliente
from .console import Console
from .acessorio import Acessorio

# carregamento dos modelos
__all__ = [
    "Jogo",
    "Plataforma",
    "JogoPlataforma",
    "Cliente",
    "Locacao",
    "ItemLocacao",
    "UtilizacaoDoConsolePeloCliente",
    "Console",
    "Acessorio"
]
