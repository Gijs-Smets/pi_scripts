import time
import board
import busio

scl_pin = board.D3
sda_pin = board.D2

i2c = busio.I2C(scl_pin, sda_pin)

ADDRESS = 0x23

COMMAND_HIGH_RES = bytearray([0x10])

def get_value(i2c_bus, addr):
    result = bytearray(2)

    i2c_bus.writeto_then_readfrom(addr, COMMAND_HIGH_RES, result)

    lux = ((result[0] << 8) | result[1]) / 1.2
    return lux

print("Starting BH1750 Light Sensor...")

try:
    while True:
        # Ensure the bus is locked before communication
        if i2c.try_lock():
            try:
                lux_val = get_value(i2c, ADDRESS)
                print(f"{lux_val:.2f} Lux")
            finally:
                i2c.unlock()

        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped by user.")