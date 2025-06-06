from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse


router = APIRouter(tags=["Root"])


@router.get(
    "/", status_code=status.HTTP_307_TEMPORARY_REDIRECT, response_class=RedirectResponse
)
async def root() -> RedirectResponse:
    return RedirectResponse("/docs")
