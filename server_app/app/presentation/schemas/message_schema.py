from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    message: str
    date: str
    time: str
    click_count: int


class MessageResponse(MessageCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
