from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from .token_utils import verify_access_token
from .schemas import TokenData
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(token)
    print(payload)
    if payload is None:
        raise credentials_exception  # Handle invalid token
    
    email: str = payload.get("sub")
    role: str = payload.get("role")
    user_id: int = payload.get("user_id")
    if email is None or role is None or user_id is None:
            raise credentials_exception
    
    return TokenData(user_id=user_id,sub=email, role=role)

def get_current_user_role(user_data = Depends(get_current_user)):
     print('jjjjjjjjjjjjjjjjjjjjjjjjjjjj')
     return user_data.role

def require_role(required_role: str):
    def role_dependency(user_role: str = Depends(get_current_user_role)):
        print(user_role ,required_role)
        if user_role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
    print('role dependederryyy')
    return role_dependency
