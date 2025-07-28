from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.service import Service
from src.schemas import SearchParams


router = APIRouter()


@router.get("/scripts/XML_daily.asp")
async def get_currency(
    params: SearchParams = Query(), service: Service = Depends(Service)
):
    if params.simulate_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return await service.get_date_rate(params._parsed_date)
