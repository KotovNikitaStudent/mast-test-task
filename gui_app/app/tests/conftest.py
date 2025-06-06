import os
import sys
from unittest.mock import MagicMock, patch
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from presentation.views.main_window import MainWindow


@pytest.fixture(autouse=True)
def ignore_qt_warnings():
    import warnings

    warnings.filterwarnings(
        "ignore", message="Failed to disconnect", category=RuntimeWarning
    )


@pytest.fixture
def mock_server_api():
    with patch("presentation.views.main_window.ServerAPI") as mock:
        instance = mock.return_value
        instance.get_messages = MagicMock(
            side_effect=lambda offset=0, limit=None, all_pages=False: [
                MagicMock(
                    message=f"Test message {i}",
                    date="2023-01-01",
                    time="12:00:00",
                    click_count=i,
                )
                for i in range(10 if all_pages else (limit or instance.default_limit))
            ]
        )
        instance.create_message = MagicMock()
        instance.default_limit = 100
        yield instance


@pytest.fixture
def main_window(qtbot, mock_server_api):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    return window


@pytest.fixture
def populate_messages(main_window):
    def _populate(count: int = 5):
        messages = []
        for i in range(count):
            message = MagicMock()
            message.message = f"Test message {i}"
            message.date = "2023-01-01"
            message.time = f"12:00:{i:02d}"
            message.click_count = i
            messages.append(message)

        main_window.message_model.update_messages(messages)
        return messages

    return _populate
