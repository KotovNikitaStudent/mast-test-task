from pydantic import BaseModel, ConfigDict
from datetime import datetime


class RecordCreate(BaseModel):
    text: str
    date: datetime
    time: str
    click_number: int


class RecordResponse(BaseModel):
    id: int
    text: str
    date: datetime
    time: str
    click_number: int

    model_config = ConfigDict(from_attributes=True)
