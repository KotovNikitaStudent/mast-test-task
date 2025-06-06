from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QListView,
    QPushButton,
    QApplication,
    QHBoxLayout,
    QProgressBar,
    QLabel,
)
from PySide6.QtCore import QDateTime, Qt
from presentation.models.message_model import MessageModel
from infra.api.server_api import ServerAPI
from domain.entities.message_entity import MessageEntity

from core.logger import get_logger


logger = get_logger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.current_offset = 0
        self.message_api = ServerAPI()
        self.setup_ui()
        self.refresh_messages()

    def setup_ui(self):
        self.setWindowTitle("Client Application with Pagination")
        self.setGeometry(100, 100, 600, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Enter message text")
        layout.addWidget(self.line_edit)

        buttons_layout = QHBoxLayout()
        self.send_button = QPushButton("Send Message")
        self.send_button.clicked.connect(self.send_message)
        buttons_layout.addWidget(self.send_button)

        self.refresh_button = QPushButton("Refresh Current Page")
        self.refresh_button.clicked.connect(self.refresh_messages)
        buttons_layout.addWidget(self.refresh_button)

        self.load_all_button = QPushButton("Load All Messages")
        self.load_all_button.clicked.connect(self.load_all_messages)
        buttons_layout.addWidget(self.load_all_button)
        layout.addLayout(buttons_layout)

        self.list_view = QListView()
        self.message_model = MessageModel()
        self.list_view.setModel(self.message_model)
        layout.addWidget(self.list_view)

        pagination_layout = QHBoxLayout()

        self.prev_button = QPushButton("← Previous")
        self.prev_button.clicked.connect(self.load_previous_page)
        pagination_layout.addWidget(self.prev_button)

        self.page_label = QLabel("Page: 1")
        pagination_layout.addWidget(self.page_label)

        self.next_button = QPushButton("Next →")
        self.next_button.clicked.connect(self.load_next_page)
        pagination_layout.addWidget(self.next_button)

        layout.addLayout(pagination_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

    def show_progress(self, visible=True):
        self.progress_bar.setVisible(visible)
        self.progress_bar.setRange(0, 0 if visible else 1)
        QApplication.processEvents()

    def send_message(self):
        self.click_count += 1
        current_datetime = QDateTime.currentDateTime()

        message = MessageEntity(
            message=self.line_edit.text(),
            date=current_datetime.toString("yyyy-MM-dd"),
            time=current_datetime.toString("hh:mm:ss"),
            click_count=self.click_count,
        )

        try:
            self.show_progress()
            self.message_api.create_message(message)
            logger.info(f"Message sent: {message.message}")
            self.line_edit.clear()
            self.refresh_messages()
        except Exception as e:
            logger.error(f"Error sending message: {e}")
        finally:
            self.show_progress(False)

    def refresh_messages(self):
        try:
            self.show_progress()
            messages = self.message_api.get_messages(offset=self.current_offset)
            self.message_model.update_messages(messages)
            self.update_pagination_info()
            logger.info(f"Messages refreshed (offset={self.current_offset})")
        except Exception as e:
            logger.error(f"Error refreshing messages: {e}")
        finally:
            self.show_progress(False)

    def load_all_messages(self):
        try:
            self.show_progress()
            messages = self.message_api.get_messages(all_pages=True)
            self.message_model.update_messages(messages)
            self.page_label.setText("All messages loaded")
            logger.info("All messages loaded")
        except Exception as e:
            logger.error(f"Error loading all messages: {e}")
        finally:
            self.show_progress(False)

    def load_previous_page(self):
        if self.current_offset > 0:
            self.current_offset -= self.message_api.default_limit
            if self.current_offset < 0:
                self.current_offset = 0
            self.refresh_messages()

    def load_next_page(self):
        self.current_offset += self.message_api.default_limit
        self.refresh_messages()

    def update_pagination_info(self):
        current_page = (self.current_offset // self.message_api.default_limit) + 1
        self.page_label.setText(f"Page: {current_page}")
        self.prev_button.setEnabled(self.current_offset > 0)


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

    def event(self, event):
        if event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                self.activeWindow().close()
                return True
            elif event.key() == Qt.Key.Key_Q and (
                event.modifiers() & Qt.KeyboardModifier.ControlModifier
            ):
                self.activeWindow().close()
                return True
        return super().event(event)
