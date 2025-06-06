import requests
from core.settings import get_settings
from domain.entities.message_entity import MessageEntity
from core.logger import get_logger


settings = get_settings()
logger = get_logger(__name__)


class ServerAPI:
    def __init__(self):
        self.base_url = f"{settings.API_URL}/messages/"
        self.default_limit = 100

    def create_message(self, message: MessageEntity) -> MessageEntity:
        try:
            response = requests.post(self.base_url, json=message.model_dump())
            response.raise_for_status()
            return MessageEntity(**response.json())
        except Exception as e:
            logger.error(f"API Error (create): {e}")
            raise

    def get_messages(
        self, offset: int = 0, limit: int | None = None, all_pages: bool = False
    ) -> list[MessageEntity]:
        try:
            if all_pages:
                return self._get_all_messages()

            params = {
                "offset": offset,
                "limit": limit if limit is not None else self.default_limit,
            }

            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return [MessageEntity(**message) for message in response.json()]
        except Exception as e:
            logger.error(f"API Error (get): {e}")
            raise

    def _get_all_messages(self) -> list[MessageEntity]:
        all_messages = []
        offset = 0

        while True:
            batch = self.get_messages(offset=offset, limit=self.default_limit)
            if not batch:
                break
            all_messages.extend(batch)
            offset += len(batch)

        return all_messages
