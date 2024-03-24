# from typing import List
# from fastapi import Depends, HTTPException, status, Path, APIRouter
# from pydantic import EmailStr
# from requests import Session
# from sqlalchemy import text

# # from sqlalchemy.exc import IntegrityError

# from src.database.models import Owner
# from src.database.db import get_db

# # from src.database.models import Owner
# from src.repository import owners as repository_owners
# from src.schemas import OwnerModel, OwnerResponse


# router = APIRouter(prefix="/owners", tags=["owners"])


# @router.get(
#     "/",
#     response_model=List[OwnerResponse],
#     name="Оримати список всіх контактів",
# )
# async def get_owners(db: Session = Depends(get_db)):
#     owners = await repository_owners.get_owners(db)
#     return owners


# @router.get(
#     "/{owner_id}",
#     response_model=OwnerResponse,
#     name="Отримати контакт по ідентифікатору",
# )
# async def get_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
#     owner = await repository_owners.get_owner_by_id(owner_id, db)
#     if owner is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
#     return owner

# @router.get(
#     "/search",
#     response_model=List[OwnerResponse],
#     name="Пошук контактів",
# )
# async def search_owners(
#     email: str = None,
#     name: str = None,
#     surname: str = None,
#     db: Session = Depends(get_db)
# ):
#     if email:
#         owners = await repository_owners.get_owner_by_email(email, db)
#     elif name and surname:
#         # Поиск по имени и фамилии
#         owners = db.query(Owner).filter_by(name=name, surname=surname).all()
#     elif name:
#         # Поиск по имени
#         owners = db.query(Owner).filter_by(name=name).all()
#     elif surname:
#         # Поиск по фамилии
#         owners = db.query(Owner).filter_by(surname=surname).all()
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="No search parameters provided"
#         )

#     if not owners:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="No owners found"
#         )

#     return owners


# @router.post(
#     "/",
#     response_model=OwnerResponse,
#     status_code=status.HTTP_201_CREATED,
#     name="Створити новий контакт",
# )
# async def create_owner(body: OwnerModel, db: Session = Depends(get_db)):
#     owner = await repository_owners.get_owner_by_email(body.email, db)
#     if owner:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT, detail="Email is exist"
#         )
#     owner = await repository_owners.create(body, db)
#     return owner


# @router.put(
#     "/{owner_id}",
#     response_model=OwnerResponse,
#     name="Оновити існуючий контакт",
# )
# async def update_owner(
#     body: OwnerModel, owner_id: int = Path(ge=1), db: Session = Depends(get_db)
# ):
#     owner = await repository_owners.update(owner_id, body, db)
#     if owner is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
#     return owner


# @router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT,
#     name="Видалити контакт",)
# async def remove_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
#     owner = await repository_owners.remove(owner_id, db)
#     if owner is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
#     return owner


from datetime import date
from typing import List
from fastapi import Body, Depends, Form, HTTPException, Query, status, Path, APIRouter
from fastapi import Form
from pydantic import EmailStr
from requests import Session
from sqlalchemy import text

from src.database.models import Owner
from src.database.db import get_db
from src.repository import owners as repository_owners
from src.schemas import (
    OwnerModel,
    OwnerResponse,
    OwnerSearchCriteria,
)

router = APIRouter(prefix="/owners", tags=["owners"])


@router.get(
    "/",
    response_model=List[OwnerResponse],
    name="Оримати список всіх контактів",
)
async def get_owners(db: Session = Depends(get_db)):
    owners = await repository_owners.get_owners(db)
    return owners


@router.get(
    "/{owner_id}",
    response_model=OwnerResponse,
    name="Отримати контакт по ідентифікатору",
)
async def get_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = await repository_owners.get_owner_by_id(owner_id, db)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return owner


@router.post(
    "/search",
    response_model=List[OwnerResponse],
    name="Пошук контактів",
)
async def search_owners(
    criteria: OwnerSearchCriteria = Body(...), db: Session = Depends(get_db)
):
    if criteria.email:
        owner = await repository_owners.get_owner_by_email(criteria.email, db)
        if owner:
            return [owner]
        else:
            return []
    elif criteria.name and criteria.surname:
        owners = (
            db.query(Owner)
            .filter_by(name=criteria.name, surname=criteria.surname)
            .all()
        )
    elif criteria.name:
        owners = db.query(Owner).filter_by(name=criteria.name).all()
    elif criteria.surname:
        owners = db.query(Owner).filter_by(surname=criteria.surname).all()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No search criteria provided",
        )

    if not owners:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No owners found"
        )

    return owners


@router.post(
    "/upcoming-birthdays",
    response_model=List[OwnerResponse],
    name="Контакти з днями народження за період",
)
async def get_upcoming_birthdays(
    start_date: date = Form(..., description="Дата початку периоду"),
    end_date: date = Form(..., description="Дата кінця періоду"),
    db: Session = Depends(get_db)
):
    owners = await repository_owners.get_upcoming_birthdays(start_date, end_date, db)
    return owners


@router.post(
    "/",
    response_model=OwnerResponse,
    status_code=status.HTTP_201_CREATED,
    name="Створити новий контакт",
)
async def create_owner(body: OwnerModel, db: Session = Depends(get_db)):
    owner = await repository_owners.get_owner_by_email(body.email, db)
    if owner:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is exist"
        )
    owner = await repository_owners.create(body, db)
    return owner


@router.put(
    "/{owner_id}",
    response_model=OwnerResponse,
    name="Оновити існуючий контакт",
)
async def update_owner(
    body: OwnerModel, owner_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    owner = await repository_owners.update(owner_id, body, db)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return owner


@router.delete(
    "/{owner_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="Видалити контакт",
)
async def remove_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = await repository_owners.remove(owner_id, db)
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return owner
