from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from app.controllers import convert_png_to_webp
import io
import logging

logging.basicConfig(level=logging.INFO)

async def send_photo(from_image_type: str, to_image_type: str, file: UploadFile = File(...)):
  try:
    image = Image.open(file.file)
    buf = io.BytesIO()

    if from_image_type == 'png' and to_image_type == 'webp':
      convert_png_to_webp(image, buf)
      buf.seek(0)

    return StreamingResponse(buf, media_type=f"image/{to_image_type}")
  except Exception as e:
    logging.error(f"Error during conversion: {e}")
    return {"error": str(e)}