import board
import pwmio
import time

led_pwm = pwmio.PWMOut(board.D12,frequency=5000,duty_cycle=0)

try:
    while True:
        for i in range(0,65525,500):
            led_pwm.duty_cycle = i
            time.sleep(0.01)
        for i in range(65525,0,-500):
            led_pwm.duty_cycle = i
            time.sleep(0.01)

finally:
    led_pwm.deinit()