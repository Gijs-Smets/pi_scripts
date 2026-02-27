import time
import board
import digitalio

pinOUT1 = digitalio.DigitalInOut(board.D23)
pinOUT2 = digitalio.DigitalInOut(board.D24)
pinIN1 = digitalio.DigitalInOut(board.D17)
pinIN2 = digitalio.DigitalInOut(board.D27)

pinOUT1.direction = digitalio.Direction.OUTPUT
pinOUT2.direction = digitalio.Direction.OUTPUT
pinIN1.direction = digitalio.Direction.INPUT
pinIN2.direction = digitalio.Direction.INPUT

pinIN1.pull = digitalio.Pull.DOWN
pinIN2.pull = digitalio.Pull.DOWN
pinOUT1.value = True
pinOUT2.value = True

while True:
    if pinIN1.value:
        pinOUT1.value = False
        pinOUT2.value = True
    if pinIN2.value:
        pinOUT1.value = True
        pinOUT2.value = False