from PIL import Image, ImageDraw
import svgwrite
import aspose.words as aw
import io
import xml.etree.ElementTree as ET
import webcolors

from app.utils import hex_to_rgb, name_to_rgb

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

# НАДО ДОРАБОТАТЬ
def convert_svg_to_image(svg_data: bytes, to_format: str, output_buffer: io.BytesIO):
  # Парсинг SVG данных
  root = ET.fromstring(svg_data.decode('utf-8'))
  
  # Извлечение размеров изображения
  width = int(root.attrib.get('width', '100').replace('px', ''))
  height = int(root.attrib.get('height', '100').replace('px', ''))

  # Создание изображения с прозрачным фоном
  image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
  draw = ImageDraw.Draw(image)

  # Рендеринг SVG элементов (ограниченный рендеринг, базовая реализация)
  for element in root:
    tag = element.tag.split('}')[-1]  # Учитываем пространство имен
    if tag == 'circle':
      cx = int(element.attrib.get('cx', 0))
      cy = int(element.attrib.get('cy', 0))
      r = int(element.attrib.get('r', 0))
      fill = element.attrib.get('fill', '#000000')
      try:
        fill = hex_to_rgb(fill) + (255,)
      except ValueError:
        fill = name_to_rgb(fill) + (255,)
      draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill=fill)
    elif tag == 'rect':
      x = int(element.attrib.get('x', 0))
      y = int(element.attrib.get('y', 0))
      width = int(element.attrib.get('width', 0))
      height = int(element.attrib.get('height', 0))
      fill = element.attrib.get('fill', '#000000')
      try:
        fill = hex_to_rgb(fill) + (255,)
      except ValueError:
        fill = name_to_rgb(fill) + (255,)
      draw.rectangle((x, y, x+width, y+height), fill=fill)
    # Добавьте больше условий для обработки других элементов SVG
  
  # Конвертация изображения в нужный формат
  if to_format == "png":
    image.save(output_buffer, format="PNG")
  elif to_format == "jpeg":
    image.convert("RGB").save(output_buffer, format="JPEG")
  elif to_format == "webp":
    image.save(output_buffer, format="WEBP")
  else:
    raise ValueError(f"Unsupported format: {to_format}")

  output_buffer.seek(0)