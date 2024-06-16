import webcolors

def hex_to_rgb(hex_color):
  """Конвертирует цвет из формата #RRGGBB или #RGB в (R, G, B)"""
  hex_color = hex_color.lstrip('#')
  if len(hex_color) == 6:
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
  elif len(hex_color) == 3:
    return tuple(int(hex_color[i]*2, 16) for i in (0, 1, 2))
  else:
    raise ValueError("Invalid hex color format")

def name_to_rgb(color_name):
  """Конвертирует именованный цвет в (R, G, B)"""
  return webcolors.name_to_rgb(color_name)