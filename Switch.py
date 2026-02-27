import time
import board
import digitalio

pinOUT = digitalio.DigitalInOut(board.D4)
pinIN = digitalio.DigitalInOut(board.D17)

pinOUT.direction = digitalio.Direction.OUTPUT
pinIN.direction = digitalio.Direction.INPUT
pinIN.pull = digitalio.Pull.UP


while True
    if not pinIN.value:
        pinOUT.value = True
    else:
        pinOUT.value = False
    time.sleep(0.1)
