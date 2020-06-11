from typing import Optional, Any

from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime


# Shared properties
class VacancyBase(BaseModel):
    title: str
    salary: Optional[dict]
    company: str


# Properties to receive on item creation
class VacancyCreate(VacancyBase):
    description: Optional[str]
    source: Optional[str]
    source_internal_id: int
    link: str


# Properties to receive on item update
class VacancyUpdate(VacancyCreate):
    pass


# Properties shared by models stored in DB
class VacancyInDBBase(VacancyBase):
    id: int
    created_at: datetime
    description: Optional[str]
    source: Optional[str]
    source_internal_id: int
    updated_at: datetime
    link: str

    class Config:
        orm_mode = True


# Properties to return to client
class VacancyOUT(VacancyInDBBase):
    pass


class RestUserBase(BaseModel):
    ip: str


class RestUserCreate(RestUserBase):
    pass


class RestUserUpdate(RestUserCreate):
    pass


class UserInDBBase(RestUserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class RestUserOUT(BaseModel):
    id: int


class SearchBase(BaseModel):
    request: str


class SearchCreate(SearchBase):
    user: int


class SearchUpdate(SearchCreate):
    pass


class SearchInDBBase(SearchBase):
    id: int
    user: int
    created_at: datetime

    class Config:
        orm_mode = True


class Search(SearchInDBBase):
    pass


class SearchInDB(SearchInDBBase):
    pass


