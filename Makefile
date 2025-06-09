ifeq ($(OS),Windows_NT)
    PYTHON = python
    PIP = python -m pip
    PYINSTALLER = python -m PyInstaller
    VENV_ACTIVATE = . venv/Scripts/activate
    VENV_DEACTIVATE = deactivate
    SHELL = cmd
    RM = del /s /q
    DIST_EXT = .exe
    BIN_PATH = Scripts
else
    PYTHON = python3
    PIP = pip
    PYINSTALLER = pyinstaller
    VENV_ACTIVATE = . venv/bin/activate
    VENV_DEACTIVATE = deactivate
    RM = rm -rf
    DIST_EXT =
    BIN_PATH = bin
endif

CLIENT_DIR = client
SERVER_DIR = server
VENV_DIR = venv
CLIENT_BIN = dist/main$(DIST_EXT)
SERVER_BIN = dist/main$(DIST_EXT)
TEST_FLAGS = -sv

.PHONY: help install-deps migrate-rollout migrate-rollback \
        build-server build-client run-server run-client \
        run-bin-server run-bin-client run-server-tests \
        run-client-tests clean venv-activate venv-deactivate \
		run-linters

help:
	@echo "Available targets:"
	@echo "  install-deps       - Install dependencies in virtual environment"
	@echo "  migrate-rollout    - Apply database migrations"
	@echo "  migrate-rollback   - Rollback database migrations"
	@echo "  build-server       - Build server executable"
	@echo "  build-client       - Build client executable"
	@echo "  run-server         - Run server in development mode"
	@echo "  run-client         - Run client in development mode"
	@echo "  run-bin-server     - Run server from built executable"
	@echo "  run-bin-client     - Run client from built executable"
	@echo "  run-server-tests   - Run server tests"
	@echo "  run-client-tests   - Run client tests"
	@echo "  clean              - Clean build artifacts"
	@echo "  venv-activate      - Activate virtual environment"
	@echo "  venv-deactivate    - Deactivate virtual environment"
	@echo "  run-linters        - Run linters"

install-deps:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_ACTIVATE) && \
	$(PIP) install -U pip && \
	$(PIP) install -r requirements.txt

venv-activate:
	@echo "Run this command manually:"
	@echo "On Windows: . venv/Scripts/activate"
	@echo "On Unix:    . venv/bin/activate"

venv-deactivate:
	@echo "Run this command manually: deactivate"

migrate-rollout:
	cd $(SERVER_DIR) && \
	$(PYTHON) migrate.py --rollout

migrate-rollback:
	cd $(SERVER_DIR) && \
	$(PYTHON) migrate.py --rollback

build-server:
	cd $(SERVER_DIR) && \
	$(PYINSTALLER) --onedir main.py

build-client:
	cd $(CLIENT_DIR) && \
	$(PYINSTALLER) --onefile main.py

run-server:
	cd $(SERVER_DIR) && \
	$(PYTHON) main.py

run-client:
	cd $(CLIENT_DIR) && \
	$(PYTHON) main.py

run-bin-server:
	cd $(SERVER_DIR) && \
	./$(SERVER_BIN)

run-bin-client:
	cd $(CLIENT_DIR) && \
	./$(CLIENT_BIN)

run-server-tests:
	cd $(SERVER_DIR) && \
	pytest $(TEST_FLAGS)

run-client-tests:
	cd $(CLIENT_DIR) && \
	pytest $(TEST_FLAGS)

clean:
	$(RM) $(CLIENT_DIR)/build $(CLIENT_DIR)/dist $(CLIENT_DIR)/*.spec
	$(RM) $(SERVER_DIR)/build $(SERVER_DIR)/dist $(SERVER_DIR)/*.spec
	$(RM) __pycache__ */__pycache__ */*/__pycache__
	$(RM) -rf $(CLIENT_DIR)/.pytest_cache
	$(RM) -rf $(SERVER_DIR)/.pytest_cache
	$(RM) -rf .ruff_cache

run-linters:
	black .
	ruff check --fix .
