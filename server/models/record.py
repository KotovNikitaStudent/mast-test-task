from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)
    time: Mapped[str] = mapped_column(nullable=False)
    click_number: Mapped[int] = mapped_column(nullable=False)
