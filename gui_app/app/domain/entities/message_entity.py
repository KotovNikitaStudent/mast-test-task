from pydantic import BaseModel


class MessageEntity(BaseModel):
    message: str
    date: str
    time: str
    click_count: int
    id: int | None = None
