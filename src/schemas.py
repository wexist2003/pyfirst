from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field


class DateRange(BaseModel):
    start_date: date
    end_date: date


class OwnerSearchCriteria(BaseModel):
    email: str = None
    name: str = None
    surname: str = None


class OwnerModel(BaseModel):
    name: str
    surname: str
    email: EmailStr
    birthday: date


class OwnerResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    birthday: date
    created_at: datetime
    updated_at: datetime

    # from db
    class Config:
        orm_mode = True
