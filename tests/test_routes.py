import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from app.app import app

client = TestClient(app)

@pytest.fixture
def png_image():
    img = Image.new('RGBA', (100, 100), color = (155, 0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf

def test_convert_png_to_webp(png_image):
    response = client.post("/api/convert/png-webp", files={"file": ("test.png", png_image, "image/png")})
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/webp"
