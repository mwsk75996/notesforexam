from datetime import datetime, timedelta
from pathlib import Path
import random

from sqlmodel import Field, Session, SQLModel, create_engine, delete, select

class Temperature(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: str
    value: float
    timestamp: str


sqlite_file = Path(__file__).with_name("database.db")
sqlite_url = f"sqlite:///{sqlite_file}"

engine = create_engine(
    sqlite_url,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def seed_fake_data(rows_per_sensor: int = 20, reset: bool = False):
    with Session(engine) as session:
        if reset:
            session.exec(delete(Temperature))
            session.commit()

        existing_temperature = session.exec(select(Temperature)).first()
        if existing_temperature is not None:
            return 0

        now = datetime.now()
        temperatures = []

        for sensor_id in ("1", "2"):
            for index in range(rows_per_sensor):
                if sensor_id == "1":
                    value = round(random.uniform(25.0, 45.0), 2)
                else:
                    value = round(random.uniform(15.0, 25.0), 2)

                timestamp = now - timedelta(minutes=index * 3)
                temperatures.append(
                    Temperature(
                        sensor_id=sensor_id,
                        value=value,
                        timestamp=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )

        session.add_all(temperatures)
        session.commit()

        return len(temperatures)


def add_fake_temperature(sensor_id: str):
    if sensor_id == "1":
        value = round(random.uniform(25.0, 45.0), 2)
    elif sensor_id == "2":
        value = round(random.uniform(15.0, 25.0), 2)
    else:
        value = round(random.uniform(15.0, 25.0), 2)

    temperature = Temperature(
        sensor_id=sensor_id,
        value=value,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    with Session(engine) as session:
        session.add(temperature)
        session.commit()
        session.refresh(temperature)

    return temperature
