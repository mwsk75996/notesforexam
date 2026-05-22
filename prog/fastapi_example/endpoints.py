from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, desc, select

from database import Temperature, add_fake_temperature, get_session, seed_fake_data

router = APIRouter()
bearer_scheme = HTTPBearer()
FAKE_TOKEN = "hemmelig-token"


def check_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.credentials != FAKE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return credentials.credentials


def check_sensor_exists(sensor_id: str, session: Session):
    statement = select(Temperature).where(Temperature.sensor_id == sensor_id)
    sensor_temperature = session.exec(statement).first()

    if sensor_temperature is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor '{sensor_id}' was not found",
        )

#-------------------------------------------------------------
@router.get("/")
def read_root():
    # Shows the endpoint of the API

    return [{"message": "Welcome to the Temperature API!"},
            {"endpoint": "/temperatureLastHour/", "description": "Get all temperature data from the last hour."},
            {"endpoint": "/temperature/sensor/{sensor_id}/lastHour/", "description": "Get temperature data from the last hour for a specific sensor."},
            {"endpoint": "/temperature/sensor/{sensor_id}/last10/", "description": "Get the last 10 temperature data points for a specific sensor."},
            {"endpoint": "/temperature/sensor/{sensor_id}/fake/", "description": "Insert one fake temperature row for a specific sensor."},
            {"endpoint": "/seedFakeData/?reset=true", "description": "Reset and insert fresh fake starter data."}
            ]

#-------------------------------------------------------------
@router.get("/temperatureLastHour/")
def select_temperatures_last_hour(
    session: Session = Depends(get_session),
    token: str = Depends(check_token),
):
    one_hour_ago = datetime.now() - timedelta(hours=1)
    timestamp_limit = one_hour_ago.strftime("%Y-%m-%d %H:%M:%S")

    statement = (
        select(Temperature)
        .where(Temperature.timestamp >= timestamp_limit)
        .order_by(desc(Temperature.timestamp))
    )

    return session.exec(statement).all()

#-------------------------------------------------------------
@router.get("/temperature/sensor/{sensor_id}/lastHour/")
def select_temperatures_last_hour_by_sensor(
    sensor_id: str,
    session: Session = Depends(get_session),
    token: str = Depends(check_token),
):
    check_sensor_exists(sensor_id, session)

    one_hour_ago = datetime.now() - timedelta(hours=1)
    timestamp_limit = one_hour_ago.strftime("%Y-%m-%d %H:%M:%S")

    statement = (
        select(Temperature)
        .where(Temperature.sensor_id == sensor_id)
        .where(Temperature.timestamp >= timestamp_limit)
        .order_by(desc(Temperature.timestamp))
    )

    return session.exec(statement).all()


#-------------------------------------------------------------
@router.get("/temperature/sensor/{sensor_id}/last10/")
def select_temperatures_last_10_by_sensor(
    sensor_id: str,
    session: Session = Depends(get_session),
    token: str = Depends(check_token),
):
    check_sensor_exists(sensor_id, session)

    statement = (
        select(Temperature)
        .where(Temperature.sensor_id == sensor_id)
        .order_by(desc(Temperature.timestamp))
        .limit(10)
    )

    temperatures = session.exec(statement).all()
    return {"sensor_id": sensor_id, "temperatures": temperatures}


#-------------------------------------------------------------
@router.post("/seedFakeData/")
def create_fake_data(
    reset: bool = False,
    rows_per_sensor: int = 20,
    token: str = Depends(check_token),
):
    inserted_rows = seed_fake_data(rows_per_sensor=rows_per_sensor, reset=reset)
    return {"inserted_rows": inserted_rows}


#-------------------------------------------------------------
@router.post("/temperature/sensor/{sensor_id}/fake/")
def create_fake_temperature(sensor_id: str, token: str = Depends(check_token)):
    temperature = add_fake_temperature(sensor_id)
    return temperature
