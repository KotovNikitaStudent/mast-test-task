from fastapi import status


class AppException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"
    extra: dict | None = None

    def __init__(
        self, status_code: int | None = None, detail: str | None = None, **kwargs
    ) -> None:
        self.status_code = self.status_code if not status_code else status_code
        self.detail = self.detail if not detail else detail
        self.extra = self.extra if not kwargs else kwargs
        super().__init__(self.detail)
