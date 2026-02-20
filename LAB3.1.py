import time
import board
import digitalio

print("hello blinky!")

board = {4 : digitalio.DigitalInOut(board.D4),
         17 : digitalio.DigitalInOut(board.D17),
         22 : digitalio.DigitalInOut(board.D22),
         27 : digitalio.DigitalInOut(board.D27)
         }

for i in board:
    board[i].direction = digitalio.Direction.OUTPUT

def ledblink(boardnum,delay=0.5):
    led = board[boardnum]
    led.value = True
    time.sleep(delay)
    led.value = False
    time.sleep(delay)

while True:
    ledblink(4,0.2)
    ledblink(4,0.2)
    ledblink(4,0.2)
    ledblink(4,0.7)
    ledblink(4,0.7)
    ledblink(4,0.7)
    ledblink(4,0.2)
    ledblink(4,0.2)
    ledblink(4,0.2)
    time.sleep(1)

