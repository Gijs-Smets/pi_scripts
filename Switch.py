import time
import board
import digitalio

pinOUT = digitalio.DigitalInOut(board.D4)
pinIN = digitalio.DigitalInOut(board.D17)

pinOUT.direction = digitalio.Direction.OUTPUT
pinIN.direction = digitalio.Direction.INPUT
pinIN.pull = digitalio.Pull.DOWN

pinOUT.value = True

while True:
    pinOUT.value = pinIN.value
    time.sleep(0.5)