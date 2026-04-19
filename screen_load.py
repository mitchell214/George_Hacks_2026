import time
from PIL import Image
from PIL import ImageDraw
import sys

import board
import digitalio
import adafruit_rgb_display.st7789 as st7789

spi = board.SPI()

cs = digitalio.DigitalInOut(board.D8)
dc = digitalio.DigitalInOut(board.D23)
rst = digitalio.DigitalInOut(board.D24)

DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 240

display = st7789.ST7789(
    spi,
    cs=cs,
    dc=dc,
    rst=rst,
    baudrate=8000000,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rotation=90,
)

def show_image(path, x=120, y=120):
    img = Image.open(path)
    img = img.rotate(-90, expand=True)
    img = img.convert("RGB")
    img = img.resize((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    draw = ImageDraw.Draw(img)
    draw.ellipse((x-3, y-3, x+3, y+3), fill=(255, 0, 0))

    display.image(img)

if __name__ == "__main__":
    IMAGE_PATH = sys.argv[1]
    x = 120
    y = 120
    try:
        x = int(sys.argv[2])
        y = int(sys.argv[3])
    except:
        pass
    show_image(IMAGE_PATH)