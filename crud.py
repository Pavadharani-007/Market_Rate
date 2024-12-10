from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
from passlib.context import CryptContext
from .schemas import MarketDataCreate
from .models import ThirdPartyData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate):
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise ValueError(f"User with username {user.username} already exists.")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    users = db.query(models.User).offset(skip).limit(limit).all()
    total_users = db.query(models.User).count()  # To add total users for pagination
    return {"users": users, "total": total_users}

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None  # Return None if user does not exist
    db.delete(user)
    db.commit()
    return user

# Tanker Data CRUD
def create_tanker_data(db: Session, data: schemas.TankerDataCreate):
    db_data = models.TankerData(**data.dict())  # Assuming your model has fields matching the schema
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_tanker_data(db: Session):
    return db.query(models.TankerData).all()

def update_tanker_data(db: Session, data_id: int, data: schemas.TankerDataUpdate):
    db_data = db.query(models.TankerData).filter(models.TankerData.id == data_id).first()
    if db_data:
        for key, value in data.dict(exclude_unset=True).items():  # Updating only non-null fields
            setattr(db_data, key, value)
        db.commit()
        db.refresh(db_data)
        return db_data
    return None

def delete_tanker_data(db: Session, data_id: int):
    db_data = db.query(models.TankerData).filter(models.TankerData.id == data_id).first()
    if db_data:
        db.delete(db_data)
        db.commit()
        return db_data
    return None

# Dry Bulk Data CRUD (same logic as tanker data)
def create_dry_bulk_data(db: Session, data: schemas.DryBulkDataCreate):
    db_data = models.DryBulkData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_dry_bulk_data(db: Session):
    return db.query(models.DryBulkData).all()

def update_dry_bulk_data(db: Session, data_id: int, data: schemas.DryBulkDataUpdate):
    db_data = db.query(models.DryBulkData).filter(models.DryBulkData.id == data_id).first()
    if db_data:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_data, key, value)
        db.commit()
        db.refresh(db_data)
        return db_data
    return None

def delete_dry_bulk_data(db: Session, data_id: int):
    db_data = db.query(models.DryBulkData).filter(models.DryBulkData.id == data_id).first()
    if db_data:
        db.delete(db_data)
        db.commit()
        return db_data
    return None

# Admin Data CRUD
def create_admin_data(db: Session, data: schemas.AdminDataCreate):
    db_data = models.AdminData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def get_admin_data(db: Session):
    return db.query(models.AdminData).all()

def update_admin_data(db: Session, data_id: int, data: schemas.AdminDataUpdate):
    db_data = db.query(models.AdminData).filter(models.AdminData.id == data_id).first()
    if db_data:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_data, key, value)
        db.commit()
        db.refresh(db_data)
        return db_data
    return None

def delete_admin_data(db: Session, data_id: int):
    db_data = db.query(models.AdminData).filter(models.AdminData.id == data_id).first()
    if db_data:
        db.delete(db_data)
        db.commit()
        return db_data
    return None

def create_third_party_data(db: Session, data: MarketDataCreate):
    db_data = ThirdPartyData(
        id=data.id,
        name=data.name,
        group=data.group,
        date=data.date,
        value=data.value
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
