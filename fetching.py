from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import get_db
from .crud import create_third_party_data
from .schemas import MarketDataCreate

# URL of the third-party API endpoint
API_URL = "https://7f55-14-97-224-214.ngrok-free.app/index"

# Function to fetch data from the third-party API and store it in the database
def fetch_and_store_data(db: Session):
    try:
        
        response = requests.get(API_URL)
        response.raise_for_status()

        data = response.json()

        # Validate the data and store it in the database
        for item in data:
            # Use your Pydantic schema for validation
            data_to_store = MarketDataCreate(
                id=item['id'],
                name=item['name'],
                group=item['group'],
                date=item['date'],
                value=item['value']
            )
            create_third_party_data(db=db, data=data_to_store)

        print(f"Data fetched and stored at {datetime.now()}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# Scheduler function to run the fetch task at 12:00 PM every day
def start_scheduled_task():
    scheduler = BackgroundScheduler()
    # Using cron expression to run the task every day at 12:00 PM
    scheduler.add_job(fetch_and_store_data, 'cron', hour=12, minute=0, args=[Depends(get_db)])
    scheduler.start()
