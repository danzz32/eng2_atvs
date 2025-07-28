from sqlalchemy.orm import Session
from app.domain.models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente: Cliente):
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def get_all(self):
        return self.db.query(Cliente).all()

    def get_by_id(self, cliente_id: int):
        return self.db.query(Cliente).filter(cliente_id == Cliente.id).first()

    def update(self, cliente_id: int, updated_data: dict):
        cliente = self.get_by_id(cliente_id)
        if cliente:
            for key, value in updated_data.items():
                setattr(cliente, key, value)
            self.db.commit()
            self.db.refresh(cliente)
        return cliente

    def delete(self, cliente: Cliente):
        cliente = self.get_by_id(cliente.id)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
