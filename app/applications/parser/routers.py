from typing import List

from fastapi import APIRouter, Request, Query

from app.applications.parser.models import RestUser, Search, Vacancy
from app.applications.parser.schemas import VacancyOUT, VacancyCreate
from app.applications.parser.utils.hh import HHParser

router = APIRouter()


@router.get("/search",
            tags=["search"],
            response_model=List[VacancyOUT],
            description='Search for vacancies',
            name='SEARCH'
            )
async def read_me(
        request: Request,
        q: str = Query(
            'python', min_length=3, title='Search request', description='Query string for the search request'
        ),
        count: int = Query(
            5, min=1, max=50, title='Limit', description='Limit for query'
        ),
        skip: int = Query(
            0, title='Skip', description='Skip data in query'
        ),
):
    client_ip = request.client.host
    rest_user = await RestUser.filter(ip=client_ip).first()
    if not rest_user:
        rest_user = await RestUser.create(ip=client_ip)
    await Search.create(user_id=rest_user.pk, request=q)
    vacs = await Vacancy.get_multi_by_q(q=q, skip=skip, limit=count)
    if len(vacs) < count:
        data = await HHParser.get_all(q)
        for vac in data:
            await Vacancy.create_or_update(VacancyCreate(**vac))
        vacs = await Vacancy.filter(description__icontains=q).limit(count).offset(skip).all()
    return vacs
