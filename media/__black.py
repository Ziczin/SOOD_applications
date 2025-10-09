from PIL import Image

def make_opaque_pixels_black(input_path: str, output_path: str):
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a != 0:
                # устанавливаем RGB в чёрный, сохраняем альфу
                pixels[x, y] = (0, 0, 0, a)
    img.save(output_path)

if __name__ == "__main__":
    # пример использования
    make_opaque_pixels_black("trash.png", "output.png")
