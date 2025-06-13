from sqlalchemy.orm import Session
from models.campeonato import Campeonato
from models.resultado import Resultado
from models.partida import Partida


class CampeonatoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Campeonato).all()

    def get_by_id(self, campeonato_id: int):
        return self.db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()

    def get_times_por_campeonato(self, campeonato_id: int):
        campeonato = self.db.query(Campeonato).filter(Campeonato.id == campeonato_id).first()
        if campeonato:
            return campeonato.times
        return []

    def create(self, campeonato: Campeonato):
        self.db.add(campeonato)
        self.db.commit()
        self.db.refresh(campeonato)
        return campeonato

    def update(self, campeonato: Campeonato):
        self.db.merge(campeonato)
        self.db.commit()
        self.db.refresh(campeonato)
        return campeonato

    def delete(self, campeonato_id: int):
        campeonato = self.get_by_id(campeonato_id)
        if campeonato:
            self.db.delete(campeonato)
            self.db.commit()
            return True
        return False

    def atualizar_classificacao(self, campeonato_id):
        # Buscar campeonato
        campeonato = self.db.query(Campeonato).filter_by(id=campeonato_id).one()

        # Inicializar pontuação dos times participantes
        pontuacoes = {time.id: 0 for time in campeonato.times}

        # Buscar partidas do campeonato que já tenham resultado
        partidas = (
            self.db.query(Partida)
            .filter_by(campeonato_id=campeonato_id)
            .join(Resultado)
            .all()
        )

        for partida in partidas:
            resultado = partida.resultado
            # Atualizar pontuação mandante
            if resultado.numGolsMandante > resultado.numGolsVisitante:
                pontuacoes[partida.timeMandante_id] += 3
            elif resultado.numGolsMandante == resultado.numGolsVisitante:
                pontuacoes[partida.timeMandante_id] += 1
                pontuacoes[partida.timeVisitante_id] += 1
            else:
                pontuacoes[partida.timeVisitante_id] += 3

        # Atualizar campo pontos do time e salvar
        for time in campeonato.times:
            time.pontos = pontuacoes[time.id]

        self.db.commit()
