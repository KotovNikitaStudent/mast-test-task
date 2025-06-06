from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from domain.entities.message_entity import MessageEntity


class MessageModel(QAbstractListModel):
    def __init__(self, messages: list[MessageEntity] = None, parent=None):
        super().__init__(parent)
        self.messages = messages or []

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.messages)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.messages)):
            return None

        message = self.messages[index.row()]

        if role == Qt.DisplayRole:
            return f"{message.date} {message.time}: {message.message} (click {message.click_count})"

        return None

    def update_messages(self, messages: list[MessageEntity]):
        self.beginResetModel()
        self.messages = messages
        self.endResetModel()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return f"Total messages: {len(self.messages)}"
        return None
