from datetime import datetime, timedelta
from typing import Optional, List

from tortoise import fields
from tortoise.exceptions import DoesNotExist

from app.applications.parser.schemas import VacancyCreate
from app.core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel


class Vacancy(BaseDBModel, BaseCreatedUpdatedAtModel):
    title = fields.TextField(null=True)
    description = fields.TextField(null=True)
    salary = fields.JSONField(null=True)
    company = fields.TextField(null=True)
    source = fields.TextField(null=True)
    source_internal_id = fields.TextField(null=True)
    link = fields.TextField(null=True)

    @classmethod
    async def get_by_internal_id(cls, internal_id: int, source: str) -> Optional["Vacancy"]:
        try:
            vacancy = await cls.get(source=source, source_internal_id=internal_id)
            return vacancy
        except DoesNotExist:
            return None

    @classmethod
    async def get_multi_by_q(cls, skip: int, limit: int, q: str) -> Optional[List["Vacancy"]]:
        return await cls.filter(description__icontains=q, updated_at__gt=datetime.now() - timedelta(days=1))\
            .offset(skip).limit(limit).all()

    @classmethod
    async def create_or_update(cls, vacancy_in: VacancyCreate) -> None:
        internal_id = vacancy_in.source_internal_id
        source = vacancy_in.source
        vacancy = await cls.get_by_internal_id(internal_id=internal_id, source=source)
        if not vacancy:
            vacancy = Vacancy(**vacancy_in.dict())
        else:
            await vacancy.update_from_dict(vacancy_in.dict())
        await vacancy.save()


class RestUser(BaseDBModel, BaseCreatedUpdatedAtModel):
    ip = fields.TextField(null=True)


class Search(BaseDBModel, BaseCreatedAtModel):
    user = fields.ForeignKeyField('models.RestUser', related_name='searches')
    request = fields.TextField()
