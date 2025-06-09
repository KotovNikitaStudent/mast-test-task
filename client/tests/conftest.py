import pytest
from PySide6.QtWidgets import QApplication
from main import MainWindow


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def app(qtbot, qapp):
    window = MainWindow()
    qtbot.addWidget(window)
    yield window
    window.close()
