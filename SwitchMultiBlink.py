import time
import board
import digitalio

print("Blinking")

switch = digitalio.DigitalInOut(board.D5)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

board = {4 : digitalio.DigitalInOut(board.D4),
         17 : digitalio.DigitalInOut(board.D17),
         22 : digitalio.DigitalInOut(board.D22),
         27 : digitalio.DigitalInOut(board.D27)
         }

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

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
    if switch.value:
        ledblink({4})
        ledblink({17})
        ledblink({27})
        ledblink({22})
    else:
        ledblink({22})
        ledblink({27})
        ledblink({17})
        ledblink({4})