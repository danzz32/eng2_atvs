from sqlalchemy.orm import Session
from models.time import Time


class TimeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Time).all()

    def get_by_id(self, time_id: int):
        return self.db.query(Time).filter(Time.id == time_id).first()

    def create(self, time: Time):
        self.db.add(time)
        self.db.commit()
        self.db.refresh(time)
        return time

    def delete(self, time_id: int):
        time = self.get_by_id(time_id)
        if time:
            self.db.delete(time)
            self.db.commit()
            return True
        return False
