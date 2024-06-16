import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image
from app.app import app

client = TestClient(app)

@pytest.fixture
def png_image():
  img = Image.new('RGBA', (100, 100), color=(155, 0, 0, 0))
  buf = io.BytesIO()
  img.save(buf, format='PNG')
  buf.seek(0)
  return buf

@pytest.mark.parametrize("from_format,to_format", [("png", "webp"), ("jpeg", "webp"), ("png", "jpeg"), ("png", "svg"), ("svg", "png"), ("svg", "jpeg"), ("svg", "webp")])
def test_supported_formats(png_image, from_format, to_format):
  if from_format == "jpeg":
    img = Image.new('RGB', (100, 100), color=(155, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    png_image = buf

  if from_format == "svg":
    test_svg = '''
      <svg height="100" width="100">
        <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="red" />
        <rect x="10" y="10" width="30" height="30" fill="blue" />
      </svg>
    '''
    png_image = io.BytesIO(test_svg.encode('utf-8'))

  response = client.post(f"/api/convert/{from_format}-{to_format}", files={"file": ("test_image", png_image, f"image/{from_format}")})
  assert response.status_code == 200
  assert response.headers["content-type"] == f"image/{to_format}" if to_format != "svg" else "image/svg+xml"