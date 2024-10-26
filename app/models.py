from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLEnum
from enum import Enum

from .database import Base

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    staff = "staff"

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone_number = Column(String)
    password = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.user)
    addresses = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key = True, index = True)
    city = Column(String)
    state = Column(String)
    street_address = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("Users", back_populates="addresses")

