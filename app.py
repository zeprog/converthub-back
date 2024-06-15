from typing import Union
from fastapi import FastAPI, File, UploadFile
from routes import send_photo
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.post('/api/convert/{from_image_type}-{to_image_type}')
async def convert(from_image_type: str, to_image_type: str, file: UploadFile = File(...)):
  return await send_photo(from_image_type, to_image_type, file)