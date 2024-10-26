from pydantic import BaseModel, EmailStr
from typing import Optional

from .models import UserRole

class TokenData(BaseModel):
    sub: str
    role: str
    user_id: int
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str 

class AddressCreate(BaseModel):
    city: str
    state: str
    street_address: str

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    password: str 
    role: Optional[UserRole] = UserRole.user

class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    addresses: list[AddressCreate] = []  # Optional list of addresses

    class Config:
        orm_mode = True  # Enable ORM mode to read data from SQLAlchemy models

