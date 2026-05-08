import time
import busio
import board
from adafruit_bus_device.i2c_device import I2CDevice

i2c = busio.I2C(board.GP1, board.GP0)
device = I2CDevice(i2c, 0x23) # i2c address

with device:
        bytes_to_write = bytearray([0x10]) # 1lx resolution 120ms see datasheet
        device.write(bytes_to_write)

while True:
    with device:
        bytes_read = bytearray(2)
        device.readinto(bytes_read)
    lux = (((bytes_read[0]&3)<<8) + bytes_read[1])/1.2 # conversion see datasheet
    print("%.2f Lux (no lib)" % lux)
    time.sleep(1)
