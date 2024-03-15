from typing import List
from fastapi import Depends, FastAPI, HTTPException, Query, status, Path
from requests import Session
from sqlalchemy import text
# from sqlalchemy.exc import IntegrityError

from db import get_db
from models import Cat, Owner
from schemas import CatModel, CatResponse, CatVaccinatedModel, OwnerModel, OwnerResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get(
    "/owners",
    response_model=List[OwnerResponse],
    name="Повернути власників",
    tags=["owners"],
)
async def get_owners(db: Session = Depends(get_db)):
    owners = db.query(Owner).all()
    return owners


@app.get("/owners/{owner_id}", response_model=OwnerResponse, tags=["owners"])
async def get_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return owner


@app.post("/owners", response_model=OwnerResponse, tags=["owners"])
async def create_owner(body: OwnerModel, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(email=body.email).first()
    if owner:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email is exist"
        )
    owner = Owner(**body.dict())
    db.add(owner)
    db.commit()
    db.refresh(owner)
    # try:
    #     owner = Owner(**body.dict())
    #     db.add(owner)
    #     db.commit()
    #     db.refresh(owner)
    # except IntegrityError as err:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is exist")
    return owner


@app.put("/owners/{owner_id}", response_model=OwnerResponse, tags=["owners"])
async def update_owner(
    body: OwnerModel, owner_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    owner.email = body.email
    db.commit()
    return owner


@app.delete(
    "/owners/{owner_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["owners"]
)
async def remove_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(owner)
    db.commit()
    return owner


@app.get(
    "/cats",
    response_model=List[CatResponse],
    tags=["cats"],
)
async def get_cats(
    limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)
):
    cats = db.query(Cat).limit(limit).offset(offset).all()
    return cats


@app.get("/cats/{cat_id}", response_model=CatResponse, tags=["cats"])
async def get_cat(cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return cat


@app.post("/cats", response_model=CatResponse, tags=["cats"])
async def create_cat(body: CatModel, db: Session = Depends(get_db)):
    cat = Cat(**body.dict())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@app.put("/cats/{cat_id}", response_model=CatResponse, tags=["cats"])
async def update_cat(
    body: CatModel, cat_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    cat.nickname = body.nickname
    cat.age = body.age
    cat.vaccinated = body.vaccinated
    cat.description = body.description
    cat.owner_id = body.owner_id
    db.commit()
    return cat


@app.delete("/cats/{cat_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["cats"])
async def remove_cat(cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(cat)
    db.commit()
    return cat


@app.patch("/cats/{cat_id}/vaccinated", response_model=CatResponse, tags=["cats"])
async def vaccinated_cat(
    body: CatVaccinatedModel, cat_id: int = Path(ge=1), db: Session = Depends(get_db)
):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    cat.vaccinated = body.vaccinated
    db.commit()
    return cat
