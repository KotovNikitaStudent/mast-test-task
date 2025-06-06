from fastapi import Depends
from sqlalchemy.orm import Session

from db.base import get_db
from db.repositories.message_repository import MessageRepository
from service.message_service import MessageService


def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    repository = MessageRepository(db)
    return MessageService(repository)
