from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from src.service import Service
from src.schemas import SearchParams


router = APIRouter()


@router.get("/scripts/XML_daily.asp", response_class=Response)
async def get_currency(
    params: SearchParams = Query(), service: Service = Depends(Service)
):
    if params.simulate_error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    xml_content = await service.get_date_rate(params.parsed_date)
    return Response(content=xml_content, media_type="application/xml")
