from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .models import Users, Address  
from .database import SessionLocal, engine  
from .models import Users, Address
from .schemas import UserCreate, AddressCreate
from .schemas import UserLogin
from .utils import  hash_password
from app import crud, token_utils, utils
from .auth import get_current_user, require_role

app = FastAPI()

# Base.metadata.create_all(bind=engine)

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=UserCreate)
async def register_user(user : UserCreate,db: Session= Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = Users(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post('/create/{user_id}/address/', response_model = AddressCreate)
async def create_address(user_id: int, address: AddressCreate, db: Session=Depends(get_db)):
    db_address = Address(**address.dict(), user_id = user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address



@app.post("/login/")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=user_credentials.username)  # Use 'username' from form data
    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = token_utils.create_acess_token(data={"sub": user.email, "role": user.role, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


#To check the authetication
@app.get("/users/me/")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"user_email": current_user}

#To check the authorization
@app.get("/user-dashboard", dependencies=[Depends(require_role("user"))])
async def read_user_dashboard():
    return {"message": "Welcome to the USER dashboard"}

@app.post("/admin-dashboard", dependencies=[Depends(require_role("admin"))])
async def read_user_dashboard():
    return {"message": "Welcome to the ADMIN dashboard"}