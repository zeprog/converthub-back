from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
from app.controllers import convert_image, convert_svg_to_image, convert_to_svg
import io
import logging

logging.basicConfig(level=logging.INFO)

SUPPORTED_FORMATS = {"png", "jpeg", "jpg", "webp", "svg"}

async def send_photo(from_image_type: str, to_image_type: str, file: UploadFile):
  if from_image_type not in SUPPORTED_FORMATS or to_image_type not in SUPPORTED_FORMATS:
    raise HTTPException(status_code=400, detail="Unsupported file format")

  try:
    buf = io.BytesIO()
    if from_image_type == "svg":
      input_svg = await file.read()
      convert_svg_to_image(input_svg, to_format=to_image_type, output_buffer=buf)
    else:
      image = Image.open(file.file)
      if to_image_type == "svg":
        convert_to_svg(image, output_buffer=buf)
      else:
        convert_image(image, to_format=to_image_type, output_buffer=buf)
    
    buf.seek(0)
    media_type = f"image/{to_image_type}" if to_image_type != "svg" else "image/svg+xml"
    return StreamingResponse(buf, media_type=media_type)
  except Exception as e:
    logging.error(f"Error during conversion: {e}")
    raise HTTPException(status_code=500, detail=str(e))