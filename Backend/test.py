import io
import json
import pytest
from app import app, session, Base, engine, User, Logs, User_Photo, Output_Photo
from sqlalchemy.orm import Session
from datetime import datetime

@pytest.fixture(scope="module")
def test_client():
    """Fixture for creating a Flask test client"""
    app.config['TESTING'] = True
    client = app.test_client()
    yield client
    
def test_signup_success(test_client):
    """Test successful user signup"""
    response = test_client.post(
        "/signup",
        json={"UserName": "tester", "Email": "test@example.com", "Password": "12345"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "Signup successful" in data["message"]
    assert data["user"]["UserName"] == "tester"


def test_signup_duplicate(test_client):
    """Test duplicate user signup"""
    response = test_client.post(
        "/signup",
        json={"UserName": "tester", "Email": "test@example.com", "Password": "12345"}
    )
    assert response.status_code == 409


def test_signup_missing_fields(test_client):
    """Test signup with missing data"""
    response = test_client.post("/signup", json={"UserName": "tester2"})
    assert response.status_code == 400


def test_login_success(test_client):
    """Test login with valid credentials"""
    response = test_client.post(
        "/login",
        json={"UserName": "tester", "Password": "12345"}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "Login successful" in data["message"]


def test_login_invalid(test_client):
    """Test login with wrong credentials"""
    response = test_client.post(
        "/login",
        json={"UserName": "tester", "Password": "wrongpass"}
    )
    assert response.status_code == 401


def test_get_all_logs_empty(test_client):
    """Test logs route when no logs exist"""
    response = test_client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_get_logs_by_user_not_found(test_client):
    """Test logs for user with no entries"""
    response = test_client.get("/logs/99999")
    assert response.status_code == 404


def test_handle_logging_upload(test_client, monkeypatch):
    """Test uploading a file and creating log entries"""

    # Mock Get_Image_Data to prevent actual image processing
    def mock_get_image_data(path):
        return {"tags": "mock_tag", "type": {"brightness": "high"}}, "mock_output.jpg"

    monkeypatch.setattr("app.Get_Image_Data", mock_get_image_data)

    # Create a dummy user first
    user = User(User_ID=12345, UserName="fileuser", Email="file@ex.com", Password="pass", Created_at=datetime.utcnow())
    session.add(user)
    session.commit()

    # Fake image file
    data = {
        "file": (io.BytesIO(b"fake image data"), "test.jpg"),
        "User_ID": "12345",
        "Title": "Mock Title",
        "Caption": "Mock Caption",
        "Location": "Mock Location"
    }

    response = test_client.post("/Handle_Logging", data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    res_json = response.get_json()
    assert "File uploaded successfully" in res_json["message"]
    assert "Photo_ID" in res_json


def test_handle_logging_no_file(test_client):
    """Test Handle_Logging with no file"""
    response = test_client.post("/Handle_Logging", data={"User_ID": "1"})
    assert response.status_code == 400
    assert "No file part" in response.get_json()["error"]
