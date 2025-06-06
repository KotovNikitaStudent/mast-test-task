import argparse

from core.logger import get_logger
from db.base import Base, engine
from db.models.message import Message  # noqa: F401


logger = get_logger(__name__)


def rollout():
    logger.info("Applying migrations...")
    Base.metadata.create_all(bind=engine)
    logger.info("Migrations applied successfully")


def rollback():
    logger.info("Rolling back migrations...")
    Base.metadata.drop_all(bind=engine)
    logger.info("Migrations rolled back successfully")


def main():
    parser = argparse.ArgumentParser(description="Database migration tool")
    parser.add_argument(
        "--rollout", action="store_true", help="Rollout migrations (create tables)"
    )
    parser.add_argument(
        "--rollback", action="store_true", help="Rollback migrations (drop tables)"
    )
    args = parser.parse_args()

    if args.rollout:
        rollout()
    if args.rollback:
        rollback()


if __name__ == "__main__":
    main()
