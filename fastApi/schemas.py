from pydantic import BaseModel, Field, EmailStr


class OwnerModel(BaseModel):
    email: EmailStr


class OwnerResponse(BaseModel):
    id: int = 1
    email: EmailStr

    # from db
    class Config:
        orm_mode = True


class CatModel(BaseModel):
    nickname: str = Field("Murchik", min_length=3, max_length=16)
    age: int = Field(1, ge=0, le=30)
    vaccinated: bool = False    
    description: str
    owner_id: int = Field(1, gt=0)

class CatVaccinatedModel(BaseModel):
    vaccinated: bool = False    


class CatResponse(BaseModel):
    id: int = 1
    nickname: str
    vaccinated: bool    
    age: int
    description: str
    owner: OwnerResponse

    # from db
    class Config:
        orm_mode = True
