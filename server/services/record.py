from db.repositories import IRecordRepository
from schemas.record import RecordCreate
from models.record import Record


class RecordService:
    def __init__(self, repo: IRecordRepository) -> None:
        self.repo = repo

    def create_record(self, record: RecordCreate) -> Record:
        return self.repo.create(record)

    def get_records(self, offset: int, limit: int) -> list[Record]:
        return self.repo.list(offset, limit)
