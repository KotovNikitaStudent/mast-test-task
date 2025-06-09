from schemas.record import RecordCreate
from models.record import Record

from sqlalchemy.orm import Session


class IRecordRepository:
    def create(self, record_create: RecordCreate) -> Record:
        raise NotImplementedError

    def list(self, offset: int, limit: int) -> list[Record]:
        raise NotImplementedError


class RecordRepository(IRecordRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, record_create: RecordCreate) -> Record:
        db_record = Record(**record_create.model_dump())
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def list(self, offset: int, limit: int) -> list[Record]:
        return self.db.query(Record).offset(offset).limit(limit).all()
