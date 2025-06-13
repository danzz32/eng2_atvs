from sqlalchemy.orm import Session
from models.resultado import Resultado


class ResultadoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Resultado).all()

    def get_by_id(self, resultado_id: int):
        return self.db.query(Resultado).filter(Resultado.id == resultado_id).first()

    def create(self, resultado: Resultado):
        self.db.add(resultado)
        self.db.commit()
        self.db.refresh(resultado)
        return resultado

    def delete(self, resultado_id: int):
        resultado = self.get_by_id(resultado_id)
        if resultado:
            self.db.delete(resultado)
            self.db.commit()
            return True
        return False
