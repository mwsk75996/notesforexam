# FastAPI example

Dette eksempel viser et lille Python API med:

- FastAPI
- SQLite database (`database.db`)
- SQLModel
- fake temperatur-data
- bearer token auth
- `TestClient` tests

## Installer dependencies

Lav og aktiver virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Installer Python pakker:

```sh
python -m pip install -r requirements.txt
```

## Start API'et

```sh
./run_api.sh
```

Eller direkte:

```sh
fastapi dev main.py
```

Docs:

```text
http://127.0.0.1:8000/docs
```

## Token

Beskyttede endpoints kræver bearer token:

```text
hemmelig-token
```

I Swagger docs:

1. Tryk `Authorize`
2. Skriv `hemmelig-token`
3. Kør endpointet

Med curl:

```sh
curl -H "Authorization: Bearer hemmelig-token" http://127.0.0.1:8000/temperature/sensor/1/last10/
```

## Fake data

Når appen starter, oprettes databasen og der indsættes fake data hvis databasen er tom.

Hvis data er blevet for gamle til `/lastHour/`, kan du reset'e:

```text
POST /seedFakeData/?reset=true
```

## Endpoints

```text
GET  /
GET  /temperatureLastHour/
GET  /temperature/sensor/{sensor_id}/lastHour/
GET  /temperature/sensor/{sensor_id}/last10/
POST /temperature/sensor/{sensor_id}/fake/
POST /seedFakeData/?reset=true
```

Hvis en sensor ikke findes i databasen, returnerer sensor-endpoints `404`.

## Kør tests

```sh
./run_tests.sh
```

Testen viser blandt andet:

- root endpoint svarer `200`
- endpoint uden token svarer `401`
- endpoint med korrekt token svarer `200`
- ukendt sensor svarer `404`
