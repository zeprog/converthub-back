from PIL import Image
import aspose.words as aw
import io

def convert_image(input_image: Image.Image, to_format: str, output_buffer: io.BytesIO):
  converters = {
    "webp": convert_to_webp,
    "jpeg": convert_to_jpeg,
    "svg": convert_to_svg,
  }

  if to_format not in converters:
    raise ValueError(f"Conversion to {to_format} is not supported")

  converters[to_format](input_image, output_buffer)

def convert_to_webp(input_image: Image.Image, output_buffer: io.BytesIO):
  if input_image.mode in ("RGBA", "LA") or (input_image.mode == "P" and "transparency" in input_image.info):
    input_image.save(output_buffer, "webp", lossless=True)
  else:
    input_image.convert("RGB").save(output_buffer, "webp")

def convert_to_jpeg(input_image: Image.Image, output_buffer: io.BytesIO):
  if input_image.mode in ("RGBA", "LA") or (input_image.mode == "P" and "transparency" in input_image.info):
    background = Image.new("RGB", input_image.size, (255, 255, 255))
    background.paste(input_image, mask=input_image.split()[3])  # 3 это альфа-канал
    background.save(output_buffer, "jpeg")
  else:
    input_image.convert("RGB").save(output_buffer, "jpeg")

def convert_to_svg(input_image: Image.Image, output_buffer: io.BytesIO):
  with io.BytesIO() as temp_png:
    input_image.save(temp_png, format='PNG')
    temp_png.seek(0)
    
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    builder.insert_image(temp_png)
    
    save_options = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)
    doc.save(output_buffer, save_options)

def convert_svg_to_image(svg_data: bytes, to_format: str, output_buffer: io.BytesIO, webp_quality: int = 80):
  with io.BytesIO() as temp_svg:
    temp_svg.write(svg_data)
    temp_svg.seek(0)

    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    shape = builder.insert_image(temp_svg)
    
    # Настройка размеров страницы и полей
    pageSetup = builder.page_setup
    pageSetup.page_width = shape.width
    pageSetup.page_height = shape.height
    pageSetup.top_margin = 0
    pageSetup.left_margin = 0
    pageSetup.bottom_margin = 0
    pageSetup.right_margin = 0
    
    if to_format == 'webp':
      temp_png = io.BytesIO()
      doc.save(temp_png, aw.SaveFormat.PNG)
      temp_png.seek(0)
      input_image = Image.open(temp_png)
      convert_to_webp(input_image, output_buffer)
    else:
      if to_format == 'png':
        save_format = aw.SaveFormat.PNG
      elif to_format == 'jpeg':
        save_format = aw.SaveFormat.JPEG
      else:
        raise ValueError(f"Unsupported format: {to_format}")

      doc.save(output_buffer, save_format)

    output_buffer.seek(0)