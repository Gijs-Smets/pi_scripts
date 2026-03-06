import time
import board
import busio
import adafruit_bh1750
import adafruit_bmp280

# Create shared I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize both sensors
light_sensor = adafruit_bh1750.BH1750(i2c)
pressure_sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)

while True:
    print("--- Sensor Readings ---")
    print(f"Light:       {light_sensor.lux:.2f} lux")
    print(f"Temperature: {pressure_sensor.temperature:.1f} °C")
    print(f"Pressure:    {pressure_sensor.pressure:.2f} hPa")
    print()
    time.sleep(2)