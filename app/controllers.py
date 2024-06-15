from PIL import Image
import io

def convert_png_to_webp(input_image: Image.Image, output_buffer: io.BytesIO):
  """
  Конвертирует изображение из формата PNG в формат WebP с сохранением прозрачности.

  :param input_image: Объект изображения PIL.
  :param output_buffer: Буфер для сохранения результата в формате WebP.
  """
  # Проверка, что изображение имеет альфа-канал (прозрачность)
  if input_image.mode in ("RGBA", "LA") or (input_image.mode == "P" and "transparency" in input_image.info):
    # Конвертация изображения в формат WebP с сохранением прозрачности
    input_image.save(output_buffer, "webp", lossless=True)
  else:
    # Если изображение не имеет альфа-канала, конвертируем его в обычный WebP
    input_image.convert("RGB").save(output_buffer, "webp")
