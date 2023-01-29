# Blink4 for W600-PICO running MicroPython 1.19 - multitasking using PWM

from machine import Pin, PWM
from time import sleep_ms


print()
print('Executing blink4.py')
print('-------------------')
print()

RUNTIME = 6000 # flash for 6 seconds
# Built in blue LED connected to pin labeled PA0 on the board
LED_ON = 0  # LOW turns the built in LED ON
LED_OFF = 1 # HIGH turns the built in LED OFF

# start blinking
pwm0 = PWM(Pin(Pin.PA_00), channel=0, freq=4, duty=128)

# do something else
for i in range(int(RUNTIME/1000)):
  sleep_ms(1000)
  print('Second', i+1)               

# stop blinking
pwm0.deinit()

# Ensure the built in LED is off at end
Pin(Pin.PA_00, Pin.OUT).on()
# Equivalent to 
#   Led = Pin(Pin.PA_00, Pin.OUT)
#   Led.value(LED_OFF)
               
