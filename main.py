from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud,  app.models as models, app.schemas as schemas, app.dependencies as dependencies
from .database import engine, get_db
from .models import Role
from .fetching import start_scheduled_task


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

# Read Users
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)

# Read Single User
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete User
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Tanker Data - CRUD operations for tanker data
@app.post("/tanker-data/", dependencies=[Depends(dependencies.require_role(Role.viewer_tanker))])
def create_tanker_data(data: schemas.TankerDataCreate, db: Session = Depends(get_db)):
    return crud.create_tanker_data(db, data)

@app.get("/tanker-data/", dependencies=[Depends(dependencies.require_role(Role.viewer_tanker))])
def read_tanker_data(db: Session = Depends(get_db)):
    return crud.get_tanker_data(db)

@app.put("/tanker-data/{data_id}/", dependencies=[Depends(dependencies.require_role(Role.viewer_tanker))])
def update_tanker_data(data_id: int, data: schemas.TankerDataUpdate, db: Session = Depends(get_db)):
    updated_data = crud.update_tanker_data(db, data_id, data)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Tanker data not found")
    return updated_data

@app.delete("/tanker-data/{data_id}/", dependencies=[Depends(dependencies.require_role(Role.viewer_tanker))])
def delete_tanker_data(data_id: int, db: Session = Depends(get_db)):
    deleted_data = crud.delete_tanker_data(db, data_id)
    if not deleted_data:
        raise HTTPException(status_code=404, detail="Tanker data not found")
    return deleted_data

# Dry Bulk Data - CRUD operations for dry bulk data
@app.post("/dry-bulk-data/", dependencies=[Depends(dependencies.require_role(Role.viewer_dry_bulk))])
def create_dry_bulk_data(data: schemas.DryBulkDataCreate, db: Session = Depends(get_db)):
    return crud.create_dry_bulk_data(db, data)

@app.get("/dry-bulk-data/", dependencies=[Depends(dependencies.require_role(Role.viewer_dry_bulk))])
def read_dry_bulk_data(db: Session = Depends(get_db)):
    return crud.get_dry_bulk_data(db)

@app.put("/dry-bulk-data/{data_id}/", dependencies=[Depends(dependencies.require_role(Role.viewer_dry_bulk))])
def update_dry_bulk_data(data_id: int, data: schemas.DryBulkDataUpdate, db: Session = Depends(get_db)):
    updated_data = crud.update_dry_bulk_data(db, data_id, data)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Dry bulk data not found")
    return updated_data

@app.delete("/dry-bulk-data/{data_id}/", dependencies=[Depends(dependencies.require_role(Role.viewer_dry_bulk))])
def delete_dry_bulk_data(data_id: int, db: Session = Depends(get_db)):
    deleted_data = crud.delete_dry_bulk_data(db, data_id)
    if not deleted_data:
        raise HTTPException(status_code=404, detail="Dry bulk data not found")
    return deleted_data

# Admin Data - CRUD operations for admin data
@app.post("/admin-data/", dependencies=[Depends(dependencies.require_role(Role.admin))])
def create_admin_data(data: schemas.AdminDataCreate, db: Session = Depends(get_db)):
    return crud.create_admin_data(db, data)

@app.get("/admin-data/", dependencies=[Depends(dependencies.require_role(Role.admin))])
def read_admin_data(db: Session = Depends(get_db)):
    return crud.get_admin_data(db)

@app.put("/admin-data/{data_id}/", dependencies=[Depends(dependencies.require_role(Role.admin))])
def update_admin_data(data_id: int, data: schemas.AdminDataUpdate, db: Session = Depends(get_db)):
    updated_data = crud.update_admin_data(db, data_id, data)
    if not updated_data:
        raise HTTPException(status_code=404, detail="Admin data not found")
    return updated_data

@app.delete("/admin-data/{data_id}/", dependencies=[Depends(dependencies.require_role(Role.admin))])
def delete_admin_data(data_id: int, db: Session = Depends(get_db)):
    deleted_data = crud.delete_admin_data(db, data_id)
    if not deleted_data:
        raise HTTPException(status_code=404, detail="Admin data not found")
    return deleted_data


@app.on_event("startup")
def on_startup():
    # Start the background task scheduler when the app starts
    start_scheduled_task()

@app.on_event("shutdown")
def on_shutdown():
    # Stop the scheduler gracefully on app shutdown
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.shutdown()