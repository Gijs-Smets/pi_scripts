import time
import board
import digitalio

print("Turning")

input = digitalio.DigitalInOut(board.D6)
input.direction = digitalio.Direction.INPUT
input.pull = digitalio.Pull.UP

board = {4 : digitalio.DigitalInOut(board.D4),
         17 : digitalio.DigitalInOut(board.D17),
         27 : digitalio.DigitalInOut(board.D27),
         22 : digitalio.DigitalInOut(board.D22)
         }

for i in board:
    board[i].direction = digitalio.Direction.OUTPUT

def step1():
    board[4].value = True
    board[27].value = False

def step2():
    board[17].value = True
    board[22].value = False

def step3():
    board[27].value = True
    board[4].value = False

def step4():
    board[22].value = True
    board[17].value = False

def fullstep(delay=0.002):
    step1()
    time.sleep(delay)
    step2()
    time.sleep(delay)
    step3()
    time.sleep(delay)
    step4()
    time.sleep(delay)

def fullstepR(delay=0.002):
    step4()
    time.sleep(delay)
    step3()
    time.sleep(delay)
    step2()
    time.sleep(delay)
    step1()
    time.sleep(delay)

while True:
    if input.value:
        fullstep()
    else:
        fullstepR()