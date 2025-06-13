class JogadorService:
    def __init__(self, jogador_repository):
        self.jogador_repository = jogador_repository

    def salvar_jogador(self, jogador):
        # Validação simples: nome não pode ser vazio
        if not jogador.nome or jogador.nome.strip() == "":
            return False

        # Aqui poderia ter outras validações, regras de negócio...

        # Se válido, chama o repositório para salvar
        self.jogador_repository.save(jogador)
        return True
