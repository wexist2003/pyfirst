from datetime import datetime, date
from pydantic import BaseModel, EmailStr


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
