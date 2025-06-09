from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.repositories import RecordRepository
from services.record import RecordService


def get_record_repository(db: Session = Depends(get_db)) -> RecordRepository:
    return RecordRepository(db)


def get_record_service(
    repo: RecordRepository = Depends(get_record_repository),
) -> RecordService:
    return RecordService(repo)
