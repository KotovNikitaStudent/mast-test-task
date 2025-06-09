from fastapi import APIRouter, Depends, Query, status

from schemas.record import RecordCreate, RecordResponse
from core.deps import get_record_service
from services.record import RecordService


router = APIRouter(prefix="/records", tags=["Records"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=RecordResponse)
def create_record(
    record: RecordCreate, service: RecordService = Depends(get_record_service)
):
    return service.create_record(record)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[RecordResponse])
def get_records(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    service: RecordService = Depends(get_record_service),
):
    return service.get_records(offset, limit)
