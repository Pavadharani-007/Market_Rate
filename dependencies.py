from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from .models import Role, User
import jwt

SECRET_KEY = "P67788j"
ALGORITHM = "HS256"

def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

def require_role(role: Role):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user
    return role_checker
