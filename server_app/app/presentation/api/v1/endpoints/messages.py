from fastapi import APIRouter, Query, Depends

from presentation.schemas.message_schema import MessageCreate, MessageResponse
from service.message_service import MessageService
from presentation.dependencies import get_message_service


router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("", response_model=list[MessageResponse])
def read_messages(
    offset: int = Query(0),
    limit: int = Query(100),
    service: MessageService = Depends(get_message_service),
):
    return service.get_messages(offset, limit)


@router.post("", response_model=MessageResponse)
def create_message(
    message: MessageCreate, service: MessageService = Depends(get_message_service)
):
    return service.create_message(message)
