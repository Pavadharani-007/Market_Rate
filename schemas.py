from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import Optional


class Role(str, Enum):
    admin = "admin"
    viewer_tanker = "viewer_tanker"
    viewer_dry_bulk = "viewer_dry_bulk"

class UserCreate(BaseModel):
    username: str
    password: str
    role: Role

class User(BaseModel):
    id: int
    username: str
    role: Role

    class Config:
        orm_mode = True


class MarketDataCreate(BaseModel):
    id: str
    name: str
    group: str
    date: date
    value: int

    class Config:
        orm_mode = True


class TankerDataCreate(BaseModel):
    name: str
    group: str
    value: float
    date: str

    class Config:
        orm_mode = True

class TankerDataUpdate(BaseModel):
    name: Optional[str] = None
    group: Optional[str] = None
    value: Optional[float] = None
    date: Optional[str] = None

    class Config:
        orm_mode = True

class DryBulkDataCreate(BaseModel):
    name: str
    group: str
    value: float
    date: str

    class Config:
        orm_mode = True

class DryBulkDataUpdate(BaseModel):
    name: Optional[str]
    group: Optional[str]
    value: Optional[float]
    date: Optional[str]

    class Config:
        orm_mode = True

class AdminDataBase(BaseModel):
    admin_name: Optional[str] = None
    data: Optional[str] = None

class AdminDataCreate(AdminDataBase):
    admin_name: str
    data: str

class AdminDataUpdate(AdminDataBase):
    pass

class AdminData(AdminDataBase):
    id: int

    class Config:
        orm_mode = True