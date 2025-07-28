from app.domain.models.console import Console
from sqlalchemy.orm import Session
from typing import List, Optional


class ConsoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, console: Console) -> Console:
        self.db.add(console)
        self.db.commit()
        self.db.refresh(console)
        return console

    def get_all(self) -> list[type[Console]]:
        return self.db.query(Console).all()

    def get_by_id(self, console_id: int) -> Optional[Console]:
        return self.db.query(Console).filter(console_id == Console.id).first()

    def update(self, console: Console) -> Console:
        self.db.commit()
        self.db.refresh(console)
        return console

    def delete(self, console: Console) -> None:
        self.db.delete(console)
        self.db.commit()
