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

def ledblink(boardnum,duty_cycle=100,blinknummer=100):
    time_high = 0.02 * (duty_cycle / 100)
    time_low = 0.02 - time_high
    for i in range(blinknummer):
        for j in boardnum:
            led = board[j]
            led.value = time_high
        time.sleep(delay)
        for j in boardnum:
            led = board[j]
            led.value = time_low      
        time.sleep(delay)

while True:
    ledblink({4,17,22,27},75,3)
    ledblink({4,17,22,27},25,3)

