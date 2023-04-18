from fastapi.testclient import TestClient 
import os
from .main import app

client: TestClient = TestClient(app)


def test_login():

    body: dict = {
        "email": "maga1271@office.proven.cat",
        "password": "12345678aA"
    }
    
    response = client.post("/users/login",body)
    
    assert response.status_code == 200
    assert response.json() == {"error": False, "message": "900", "data": ""}