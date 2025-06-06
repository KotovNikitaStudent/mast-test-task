from db.repositories.message_repository import MessageRepository
from domain.entities.message_entity import MessageEntity


class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def create_message(self, message: MessageEntity) -> MessageEntity:
        return self.repository.create(message)

    def get_messages(self, offset: int = 0, limit: int = 100) -> list[MessageEntity]:
        return self.repository.get_all(offset, limit)
