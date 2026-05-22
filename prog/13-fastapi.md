# FastAPI, SQLite og API tests

Repo-eksempel i denne mappe:

- `fastapi_example/`

FastAPI er et Python framework til at lave HTTP API'er. Det bruges typisk sammen med en ASGI-server som `uvicorn`, men man kan starte det nemt med FastAPI CLI:

```sh
fastapi dev main.py
```

## Vigtige ord

- Endpoint: en URL som API'et svarer på, fx `/temperatureLastHour/`
- Route: Python-funktionen bag et endpoint
- GET: hent data
- POST: opret eller ændr data
- Status code: HTTP-resultat, fx `200`, `401`, `404`
- JSON: formatet API'et typisk sender tilbage
- Dependency: FastAPI-funktion der automatisk kaldes, fx database-session eller auth-check

## Minimal FastAPI app

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello API"}
```

Kør:

```sh
fastapi dev main.py
```

Docs:

```text
http://127.0.0.1:8000/docs
```

## APIRouter

I større projekter er det bedre at dele koden op.

`main.py`:

```python
from fastapi import FastAPI

import endpoints

app = FastAPI()
app.include_router(endpoints.router)
```

`endpoints.py`:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "OK"}
```

God eksamensforklaring:

`main.py` ejer selve appen, og `endpoints.py` ejer routes. `include_router` kobler routes på appen.

## SQLite med SQLModel

SQLModel kombinerer database-modeller og Pydantic-style Python typer.

```python
from sqlmodel import Field, SQLModel

class Temperature(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: str
    value: float
    timestamp: str
```

`table=True` betyder, at modellen bliver til en database-tabel.

SQLite setup:

```python
engine = create_engine(
    "sqlite:///database.db",
    connect_args={"check_same_thread": False},
)
```

Opret tabeller:

```python
SQLModel.metadata.create_all(engine)
```

## Database session

En session bruges til at snakke med databasen.

```python
def get_session():
    with Session(engine) as session:
        yield session
```

I et endpoint:

```python
def endpoint(session: Session = Depends(get_session)):
```

FastAPI kalder automatisk `get_session()` og giver endpointet en database-session.

## SELECT med SQLModel

```python
statement = (
    select(Temperature)
    .where(Temperature.sensor_id == sensor_id)
    .order_by(desc(Temperature.timestamp))
    .limit(10)
)

temperatures = session.exec(statement).all()
```

Dette svarer til at hente de sidste 10 temperaturer for en sensor.

## HTTPException

Hvis noget ikke findes, kan API'et returnere en rigtig HTTP-fejl:

```python
raise HTTPException(
    status_code=404,
    detail=f"Sensor '{sensor_id}' was not found",
)
```

Eksempel:

```json
{
  "detail": "Sensor '3' was not found"
}
```

## Bearer token

Eksemplet bruger en simpel fast bearer token:

```python
bearer_scheme = HTTPBearer()
FAKE_TOKEN = "hemmelig-token"
```

Hvis token er forkert:

```python
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication token",
    headers={"WWW-Authenticate": "Bearer"},
)
```

Header:

```text
Authorization: Bearer hemmelig-token
```

I Swagger docs trykker man `Authorize` og skriver kun:

```text
hemmelig-token
```

## TestClient

FastAPI kan testes uden browser:

```python
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
```

Med token:

```python
headers = {"Authorization": "Bearer hemmelig-token"}
response = client.get("/temperature/sensor/1/last10/", headers=headers)
assert response.status_code == 200
```

## Typiske fejlkoder

- `200 OK`: request virkede
- `401 Unauthorized`: mangler token eller token er forkert
- `404 Not Found`: fx sensor findes ikke
- `500 Internal Server Error`: fejl i server-koden

## Eksamensforklaring

FastAPI modtager en HTTP request, matcher URL'en til et endpoint, kører dependencies som auth og database-session, laver et database-query med SQLModel og returnerer resultatet som JSON.
