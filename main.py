from PIL import Image
from urllib.request import urlopen
import sys

IMAGE_SUFFIX = "=x{x}-y{y}-z{zoom}"
MAX_X = 4
MAX_Y = 5
BLACK = (0, 0, 0)


def main():
    if len(sys.argv) != 2:
        sys.exit("URL is required")

    filename = "sample.jpg"
    download(sys.argv[1].split("=", 1)[0], filename)
    delete_black(filename)


def download(url, name, zoom=3):
    sources = {}
    for x in range(MAX_X):
        for y in range(MAX_Y):
            im_url = urlopen(url + IMAGE_SUFFIX.format(x=x, y=y, zoom=zoom))
            sources[y, x] = Image.open(im_url)

    width = sources[0, 0].size[0]
    height = sources[0, 0].size[1]

    image_processed = Image.new("RGB", (MAX_X * width, MAX_Y * height))
    pixels_processed = image_processed.load()

    for i in range(MAX_Y):
        for j in range(MAX_X):
            pixels = sources[i, j].load()
            for x in range(width):
                for y in range(height):
                    pixels_processed[j * width + x, i * height + y] = pixels[x, y]

    image_processed.save(name)


def delete_black(filename):
    img = Image.open(filename)
    width, height = img.size
    dx = width
    pixels = img.load()
    for x in range(width - 1, -1, -1):
        fl = False
        for y in range(height):
            if pixels[x, y] != BLACK:
                fl = True
                dx = x
                break
        if fl:
            break

    output = img.crop((0, 0, dx, height))
    output.save(filename)


if __name__ == "__main__":
    main()