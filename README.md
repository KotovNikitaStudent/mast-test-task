# mast-test-task

Реализация тестового задания с клиент-серверной архитектурой. Проект включает:

- Клиент с GUI (PySide6)
- Сервер на FastAPI
- SQLite базу с SQLAlchemy
- Набор тестов
- Сборку в исполняемые файлы

## Технологии

| Компонент       | Технологии                                  |
| --------------- | ------------------------------------------- |
| **Клиент**      | PySide6, requests,                          |
| **Сервер**      | FastAPI, SQLAlchemy, Pydantic, SQLite       |
| **Инструменты** | pyinstaller, black, ruff, pytest, pytest-qt |

## Быстрый старт

```bash
git clone https://github.com/KotovNikitaStudent/mast-test-task.git
cd mast-test-task/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Запуск сервера

```bash
cd server/
python migrate.py --rollout  # Инициализация БД
python main.py              # Запуск сервера (http://0.0.0.0:8000)
```

### Запуск клиента

```bash
cd client/
python main.py
```

## Сборка

```bash
# Сервер (onedir)
cd server/
pyinstaller --onedir main.py

# Клиент (onefile)
cd client/
pyinstaller --onefile main.py
```

Собранные приложения будут в папках `server/dist/main/main` и `client/dist/main`.

```bash
# Сервер
cd server/
./dist/main/main

# Клиент
cd client/
./dist/main/
```

## Тестирование

```bash
# Тесты сервера
cd server/ && pytest -sv

# Тесты клиента
cd client/ && pytest -sv

# Проверка стиля
black --check . && ruff check .
```

## Дополнительные команды make

При установленном Make:

```bash
make help
```
