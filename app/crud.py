from sqlalchemy.orm import Session

from . import models, schemas

def create_address(db: Session, address = schemas.AddressCreate):
    pass

def get_user_by_email(db: Session, email :str):
    return db.query(models.Users).filter(models.Users.email == email).first()