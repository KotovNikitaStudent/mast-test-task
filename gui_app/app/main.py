import sys
from core.logger import get_logger
from presentation.views.main_window import Application, MainWindow


logger = get_logger(__name__)


def main():
    app = Application(sys.argv)
    window = MainWindow()
    logger.info("Client application started")
    window.show()
    window.setWindowTitle("Client Application (Ctrl+Q or Esc to exit)")
    logger.info("Window displayed")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
