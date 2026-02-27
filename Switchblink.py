import time
import board
import digitalio

pinOUT = digitalio.DigitalInOut(board.D4)
pinIN = digitalio.DigitalInOut(board.D17)

pinOUT.direction = digitalio.Direction.OUTPUT
pinIN.direction = digitalio.Direction.INPUT


# pinIN.pull = digitalio.Pull.DOWN

# while True:
#     while not pinIN.value:   
#         pinOUT.value = True
#         time.sleep(0.3)
#         pinOUT.value = False
#         time.sleep(0.3)
#     time.sleep(0.3)

pinIN.pull = digitalio.Pull.UP

while True:
    while pinIN.value:   
        pinOUT.value = True
        time.sleep(0.3)
        pinOUT.value = False
        time.sleep(0.3)
    time.sleep(0.3)