import time
import board
import digitalio

print("Changing intensity")

board = {4 : digitalio.DigitalInOut(board.D4),
         17 : digitalio.DigitalInOut(board.D17),
         22 : digitalio.DigitalInOut(board.D22),
         27 : digitalio.DigitalInOut(board.D27)
         }

for i in board:
    board[i].direction = digitalio.Direction.OUTPUT

def ledblink(boardnum,duty_cycle=100,blinknummer=100):
    time_high = 0.01 * (duty_cycle / 100)
    time_low = 0.01 - time_high
    for i in range(blinknummer):
        for j in boardnum:
            led = board[j]
            led.value = True
        time.sleep(time_high)
        for j in boardnum:
            led = board[j]
            led.value = False      
        time.sleep(time_low)

while True:
    ledblink({4,17,22,27},90,10)
    ledblink({4,17,22,27},10,10)

