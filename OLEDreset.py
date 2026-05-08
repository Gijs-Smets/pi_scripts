import time
import board
import digitalio

# ── Pins ───────────────────────────────────────────────────────
reset = digitalio.DigitalInOut(board.D26)   # GPIO26 → RES
reset.direction = digitalio.Direction.OUTPUT

# ── Reset sequence (SSD1306 datasheet) ────────────────────────
print("Resetting OLED...")

reset.value = True    # start high
time.sleep(0.001)     # 1 ms

reset.value = False   # pull low  → triggers reset
time.sleep(0.010)     # hold low for 10 ms

reset.value = True    # release high → display initialises
time.sleep(0.100)     # wait 100 ms for init to complete

print("Reset done.")