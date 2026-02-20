import time
import board
import digitalio

print("hello blinky!")

led = digitalio.DigitalInOut(board.D17)
led.direction = digitalio.Direction.OUTPUT
led2 = digitalio.DigitalInOut(board.D27)
led2.direction = digitalio.Direction.OUTPUT

while true :
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
    led2.value = True
    time.sleep(0.5)
    led2.value = False
    time.sleep(0.5)
