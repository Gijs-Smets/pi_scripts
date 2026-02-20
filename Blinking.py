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

def ledblink(boardnum,delay=0.5,blinknummer=1):
    for i in range(blinknummer):
        for j in boardnum:
            led = board[j]
            led.value = True
        time.sleep(delay)
        for j in boardnum:
            led = board[j]
            led.value = False      
        time.sleep(delay)

while True:
    ledblink({4,17,22,27},0.2,3)
    ledblink({4,17,22,27},0.7,3)
    ledblink({4,17,22,27},0.2,3)
    time.sleep(1)
