from sqlalchemy.orm import Session

from domain.entities.message_entity import MessageEntity
from db.models.message import Message


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, message: MessageEntity) -> Message:
        db_message = Message(**message.model_dump())
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Message]:
        return self.db.query(Message).offset(offset).limit(limit).all()
