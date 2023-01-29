# Blink for W600-PICO running MicroPython 1.19

from machine import Pin
from time import sleep_ms as delay

print()
print('Executing blink.py')
print('------------------')
print()

RUNS = 5         # number of flash cycles to run
CYCLES = 8       # number of quick flashes per cycle
FLASH_TIME = 100 # 100 ms on/off time of quick flashes
OFF_TIME = 1500  # 1500 ms off time between series of flashes
VERBOSE = True   # print state of LED to the serial port
LED_ON  = 0      # LOW turns the built in LED ON
LED_OFF = 1      # HIGH turns the built in LED OFF

# Built in blue LED connected to pin labeled PA0 on the board
Led = Pin(Pin.PA_00, Pin.OUT)

# Ensure the built in LED is off to start (it should be after reset)
Led.value(LED_OFF)

for j in range(RUNS):
  if VERBOSE:
    print(j+1, '/', RUNS,'  ', end='')
  for i in range(CYCLES):
    Led.value(LED_ON)
    if VERBOSE:
      print('ON ', end='')
    delay(FLASH_TIME)
    Led.value(not Led.value())
    delay(FLASH_TIME)
  if VERBOSE:
    print('OFF.')
  delay(OFF_TIME)
  
if VERBOSE:   
  print("Done.") 