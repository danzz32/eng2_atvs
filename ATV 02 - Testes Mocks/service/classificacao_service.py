class ClassificacaoService:
    def __init__(self, partida_repo, time_repo):
        self.partida_repo = partida_repo
        self.time_repo = time_repo

    def calcular_classificacao(self):
        times = self.time_repo.get_all()
        partidas = self.partida_repo.get_all()

        tabela = {}
        for time in times:
            tabela[time.id] = {
                'time': time,
                'pontos': 0,
                'jogos': 0,
                'vitorias': 0,
                'empates': 0,
                'derrotas': 0
            }

        for partida in partidas:
            mandante = partida.timeMandante
            visitante = partida.timeVisitante
            resultado = partida.resultado

            if not resultado:
                continue

            tabela[mandante.id]['jogos'] += 1
            tabela[visitante.id]['jogos'] += 1

            pontosMandante = resultado.getPontuacaoMandante()
            pontosVisitante = resultado.getPontuacaoVisitante()

            tabela[mandante.id]['pontos'] += pontosMandante
            tabela[visitante.id]['pontos'] += pontosVisitante

            if pontosMandante == 3:
                tabela[mandante.id]['vitorias'] += 1
                tabela[visitante.id]['derrotas'] += 1
            elif pontosVisitante == 3:
                tabela[visitante.id]['vitorias'] += 1
                tabela[mandante.id]['derrotas'] += 1
            else:
                tabela[mandante.id]['empates'] += 1
                tabela[visitante.id]['empates'] += 1

        # Ordenar por pontos decrescente
        resultado_final = sorted(tabela.values(), key=lambda x: x['pontos'], reverse=True)
        return resultado_final
