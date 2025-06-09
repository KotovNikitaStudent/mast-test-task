import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QListView,
    QPushButton,
    QSpinBox,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import QStringListModel
import requests
from datetime import datetime

from core.settings import get_settings
from core.logger import get_logger


settings = get_settings()
logger = get_logger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client App")
        self.click_count = 0
        self.offset = 0
        self.limit = settings.PAGINATION_LIMIT

        layout = QVBoxLayout()

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text to send")

        self.list_view = QListView()
        self.model = QStringListModel()
        self.list_view.setModel(self.model)

        self.post_button = QPushButton("Send POST")
        self.get_button = QPushButton("Get Records")

        pagination_layout = QHBoxLayout()
        self.page_label = QLabel(self._get_page_label())
        self.page_input = QSpinBox()
        self.page_input.setMinimum(0)
        self.page_input.setSingleStep(self.limit)
        self.page_input.setValue(self.offset)
        self.prev_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.page_input)
        pagination_layout.addWidget(self.prev_button)
        pagination_layout.addWidget(self.next_button)

        layout.addWidget(self.text_input)
        layout.addWidget(self.list_view)
        layout.addWidget(self.post_button)
        layout.addWidget(self.get_button)
        layout.addLayout(pagination_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.post_button.clicked.connect(self.send_post_request)
        self.get_button.clicked.connect(self.get_records)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.page_input.valueChanged.connect(self.change_offset)

    def _get_page_label(self):
        return f"Offset: {self.offset}"

    def send_post_request(self):
        self.click_count += 1
        current_time = datetime.now()
        data = {
            "text": self.text_input.text(),
            "date": current_time.isoformat(),
            "time": current_time.strftime("%H:%M:%S"),
            "click_number": self.click_count,
        }
        try:
            response = requests.post(f"{settings.server_url}/records/", json=data)
            response.raise_for_status()
            self.model.setStringList([f"POST successful: Click #{self.click_count}"])
            logger.info(f"POST successful: Click #{self.click_count}")
        except requests.RequestException as e:
            self.model.setStringList([f"Error: {str(e)}"])
            logger.error(f"Error: {str(e)}")

    def get_records(self):
        try:
            response = requests.get(
                f"{settings.server_url}/records/",
                params={"offset": self.offset, "limit": self.limit},
            )
            response.raise_for_status()
            records = response.json()
            if not records:
                self.model.setStringList(["No records found"])
                return
            display_data = [
                f"ID: {r['id']}, Text: {r['text']}, Date: {r['date']}, Click: {r['click_number']}"
                for r in records
            ]
            self.model.setStringList(display_data)
            self.page_label.setText(self._get_page_label())
            self.page_input.setValue(self.offset)
            logger.info(f"GET successful: Offset {self.offset}")
        except requests.RequestException as e:
            self.model.setStringList([f"Error: {str(e)}"])
            logger.error(f"Error: {str(e)}")

    def prev_page(self):
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.get_records()

    def next_page(self):
        self.offset += self.limit
        self.get_records()

    def change_offset(self):
        new_offset = self.page_input.value()
        if new_offset != self.offset:
            self.offset = new_offset
            self.get_records()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
