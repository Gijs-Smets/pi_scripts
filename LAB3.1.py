import time
import board
import digitalio

print("hello blinky!")

board4 = digitalio.DigitalInOut(board.D4)
board17 = digitalio.DigitalInOut(board.D17)
board27 = digitalio.DigitalInOut(board.D27)
board22 = digitalio.DigitalInOut(board.D22)

board4.direction = board17.direction = board27.direction = board22.direction = digitalio.Direction.OUTPUT

def ledblink(boardnum):
    if boardnum == 4:
        led = board4
    elif boardnum == 17:
        led = board17
    elif boardnum == 27:
        led = board27
    elif boardnum == 22:
        led = board22

    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

while True:
    ledblink(4)
    ledblink(17)
    ledblink(27)
    ledblink(22)
    ledblink(27)
    ledblink(17)

