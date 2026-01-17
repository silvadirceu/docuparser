from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_process_mock_pdf():
    # Simulate a PDF upload
    files = {'file': ('test.pdf', b'%PDF-1.4 mock content', 'application/pdf')}
    response = client.post("/process", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["detected_type"] == "digital_pdf"
    assert "tools_used" in json_data


def test_process_mock_image():
    # Simulate an image upload
    files = {'file': ('test.png', b'mock image content', 'image/png')}
    response = client.post("/process", files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["detected_type"] == "image"
