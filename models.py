from sqlalchemy import Column, Integer, String, Enum, Date, Float
from .database import Base
import enum

class Role(str, enum.Enum):
    admin = "admin"
    viewer_tanker = "viewer_tanker"
    viewer_dry_bulk = "viewer_dry_bulk"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)

class ThirdPartyData(Base):
    __tablename__ = "third_party_data"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    group = Column(String)
    date = Column(Date)
    value = Column(Integer)

class TankerData(Base):
    __tablename__ = "tanker_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    capacity = Column(Float)
    type = Column(String)

class DryBulkData(Base):
    __tablename__ = "dry_bulk_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Float)
    type = Column(String)

class AdminData(Base):
    __tablename__ = "admin_data"
    id = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String, index=True)
    data = Column(String)