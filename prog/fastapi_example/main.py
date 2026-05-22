from fastapi import FastAPI

import endpoints
from database import create_db_and_tables, seed_fake_data

app = FastAPI()
app.include_router(endpoints.router)

create_db_and_tables()
seed_fake_data()

if __name__ == "__main__":
    print("Start serveren med: fastapi dev main.py")
