import datetime

from models.jogador import Jogador
from models.time import Time
from repository.jogador_repository import JogadorRepository
from repository.time_repository import TimeRepository


def test_criar_jogador_e_persistir(db_session):
    # Criar e persistir um Time antes (FK obrigatória)
    time_repo = TimeRepository(db_session)
    time = Time(nome="Time Teste")
    time_repo.create(time)

    # Criar jogador com data no tipo correto
    jogador = Jogador(
        nome="Carlos",
        nascimento=datetime.date(2000, 1, 1),
        genero="M",
        altura=180,
        time_id=time.id
    )

    jogador_repo = JogadorRepository(db_session)
    jogador_repo.create(jogador)

    # Verifica se jogador tem ID e dados persistidos corretamente
    assert jogador.id is not None
    jogador_salvo = jogador_repo.get_by_id(jogador.id)

    assert jogador_salvo.nome == "Carlos"
    assert jogador_salvo.nascimento == datetime.date(2000, 1, 1)
    assert jogador_salvo.genero == "M"
    assert jogador_salvo.altura == 180
    assert jogador_salvo.time_id == time.id

    # Imprime o jogador salvo no banco para verificação
    print(
        f"\nJogador salvo: id={jogador_salvo.id}, nome={jogador_salvo.nome}, nascimento={jogador_salvo.nascimento}, genero={jogador_salvo.genero}, altura={jogador_salvo.altura}, time_id={jogador_salvo.time_id}")


def test_busca_jogador_por_nome(db_session):
    time_repo = TimeRepository(db_session)
    time = Time(nome="Time Teste")
    time_repo.create(time)

    jogador_repo = JogadorRepository(db_session)

    # Criar e persistir múltiplos jogadores
    jogadores = [
        Jogador(nome="Carlos Silva", nascimento=datetime.date(2000, 1, 1), genero="M", altura=180, time_id=time.id),
        Jogador(nome="Carla Souza", nascimento=datetime.date(1998, 5, 15), genero="F", altura=170, time_id=time.id),
        Jogador(nome="Roberto Carlos", nascimento=datetime.date(1995, 7, 20), genero="M", altura=175, time_id=time.id),
        Jogador(nome="Ana Maria", nascimento=datetime.date(1992, 3, 30), genero="F", altura=165, time_id=time.id),
    ]

    for jogador in jogadores:
        jogador_repo.create(jogador)

    # Busca por nome contendo "Carlos"
    resultados = jogador_repo.get_by_name("Carlos")

    # Devemos receber 2 jogadores: "Carlos Silva" e "Roberto Carlos"
    nomes_encontrados = {j.nome for j in resultados}
    assert "Carlos Silva" in nomes_encontrados
    assert "Roberto Carlos" in nomes_encontrados
    assert len(resultados) == 2

    # Imprime os jogadores encontrados para conferência
    for jogador in resultados:
        print(f"\nEncontrado: id={jogador.id}, nome={jogador.nome}")


def test_atualizar_dados_jogador(db_session):
    repo = JogadorRepository(db_session)

    # Cria e persiste jogador
    jogador = Jogador(
        nome="Carlos Silva",
        nascimento=datetime.date(2000, 1, 1),
        genero="Masculino",
        altura=180
    )
    repo.create(jogador)
    print(f"\nDados do jogador: id={jogador.id}, nome={jogador.nome}, nascimento={jogador.nascimento}, genero={jogador.genero}, altura={jogador.altura}")

    # Atualiza dados
    jogador.altura = 185
    jogador.nome = "Carlos A. Silva"
    repo.update(jogador)  # Supondo que seu repositório tenha esse metodo

    # Busca novamente
    jogador_atualizado = db_session.query(Jogador).filter_by(id=jogador.id).first()

    # Verificações
    assert jogador_atualizado is not None
    assert jogador_atualizado.nome == "Carlos A. Silva"
    assert jogador_atualizado.altura == 185
    assert jogador_atualizado.nascimento == datetime.date(2000, 1, 1)

    print(
        f"\nDados do jogador: id={jogador.id}, nome={jogador.nome}, nascimento={jogador.nascimento}, genero={jogador.genero}, altura={jogador.altura}")
