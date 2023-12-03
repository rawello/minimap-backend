import os
import glob
from PIL import Image
import wand.image
def image_to_svg(img_path):
    img = Image.open(img_path)
    width, height = img.size

    if img.mode != 'RGB':
        img = img.convert('RGB')

    res = "<?xml version = \"1.0\"?>"
    #res += "<!-- made by Максим Сергеевич, Кирилл, Сеня Арсений Сенечка, Валерия Николаевна, и просто ворон -->"
    res += f"<svg width=\"{width}\" height=\"{height}\" "
    res += "xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">"
    for y in range(height):
        for x in range(width):
            color = img.getpixel((x, y))
            if color[:3] != (255, 255, 255):
                hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
                res += f"<rect x=\"{x}\" y=\"{y}\" width=\"1\" height=\"1\" fill=\"{hex_color}\" />"
            else:
                continue

    res += "</svg>"
    return res

def convert2svg(directory):
    png_files = glob.glob(os.path.join(directory, '*.png'))

    for png_file in png_files:
        svg_data = image_to_svg(png_file)

        svg_file = os.path.splitext(png_file)[0] + '.svg'

        with open(svg_file, 'w') as f:
            f.write(svg_data)

def convert2png(directory, filename):
    with open(os.path.join(directory, filename), 'rb') as file:
        svg_blob = file.read()

    with wand.image.Image(blob=svg_blob, format='svg', colorspace='rgb') as image:
        png_image = image.make_blob('png')

    words = filename.split('.')
    result = '.'.join(words[:-1])
    with open(os.path.join(directory, result + '.png'), 'wb') as out:
        out.write(png_image)