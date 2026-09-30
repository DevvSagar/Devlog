from fastapi import FastAPI
from fastapi.testclient import TestClient

demo_app = FastAPI()

@demo_app.get("/")
def demo_home():
    return{"message":"Hello"}

client = TestClient(demo_app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200


#  Test demo file no production test are being done here ..... 