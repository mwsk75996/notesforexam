from fastapi.testclient import TestClient

from main import app


#-------------------------------------------------------------
client = TestClient(app)
auth_headers = {"Authorization": "Bearer hemmelig-token"}

def test_read_main():
    rootresponse = client.get("/")
    assert rootresponse.status_code == 200
    print(rootresponse.json())

    response = client.get("/temperatureLastHour/")
    assert response.status_code == 401
    print(response.json())

    response = client.get("/temperatureLastHour/", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

    response = client.get("/temperature/sensor/1/lastHour/", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

    response = client.get("/temperature/sensor/1/last10/", headers=auth_headers)
    assert response.status_code == 200
    print(response.json())

    response = client.get("/temperature/sensor/does-not-exist/last10/", headers=auth_headers)
    assert response.status_code == 404
    print(response.json())

if __name__ == "__main__":
    test_read_main()
