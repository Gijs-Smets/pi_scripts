import board
import digitalio
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# ── Pin configuration ──────────────────────────────────────────
RESET_PIN = digitalio.DigitalInOut(board.D26)   # GPIO26 → RES
DC_PIN    = digitalio.DigitalInOut(board.D16)   # GPIO16 → DC

# ── SPI bus ────────────────────────────────────────────────────
# baudrate can be lowered to 1_000_000 if you get glitches
spi = busio.SPI(board.SCK, MOSI=board.MOSI)

# ── Display init — pass None for CS, hardware CE0 handles it ───
oled = adafruit_ssd1306.SSD1306_SPI(
    128, 64,
    spi,
    DC_PIN,
    RESET_PIN,
    cs=None,          # <-- fixes "GPIO busy" on CE0
)

# ── Clear screen ───────────────────────────────────────────────
oled.fill(0)
oled.show()

# ── Create image canvas ────────────────────────────────────────
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# ── Border ─────────────────────────────────────────────────────
draw.rectangle((0, 0, oled.width - 1, oled.height - 1), outline=1, fill=0)

# ── Text ───────────────────────────────────────────────────────
try:
    font       = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
except IOError:
    font = font_small = ImageFont.load_default()

draw.text((4, 4),  "Hello, Pi 5!",   font=font,       fill=1)
draw.text((4, 24), "SSD1306 OLED",   font=font_small, fill=1)
draw.text((4, 38), "SPI working OK", font=font_small, fill=1)

# ── Small filled circle ────────────────────────────────────────
draw.ellipse((100, 44, 122, 60), outline=1, fill=1)

# ── Push to display ────────────────────────────────────────────
oled.image(image)
oled.show()

print("Done — check your OLED screen!")