from pydantic import BaseModel, ConfigDict


class MessageEntity(BaseModel):
    message: str
    date: str
    time: str
    click_count: int

    model_config = ConfigDict(from_attributes=True)
