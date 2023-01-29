# Blink3 for W600-PICO running MicroPython 1.19 - multitasking using Timer

from machine import Pin, Timer
from time import ticks_ms, sleep_ms
import random

print()
print('Executing blink3.py')
print('-------------------')
print()

RUNTIME = 6000 # flash for 6 seconds
PERIOD = 250   # flash on/off time
LED_ON = 0  # LOW turns the built in LED ON
LED_OFF = 1 # HIGH turns the built in LED OFF

# Built in blue LED connected to pin labeled PA0 on the board
Led = Pin(Pin.PA_00, Pin.OUT)

# Ensure the built in LED is off to start (it should be after reset)
Led.value(LED_OFF)

# Create timer instance that will toggle the built in LED
timer1 = Timer(1)

# timer1 callback function
def LedToggle(t):
    lv = 1 - Led.value()
    Led.value(lv)

# function to initialize timer1
def StartLedBlinking():
    print("Start blinking LED")
    # inititate a periodic timer which will exectute LedToggle after PERIOD ms
    timer1.init(period=PERIOD, mode=Timer.PERIODIC, callback=LedToggle)

# function to stop timer1
def StopLedBlinking():
    if Led.value() == LED_ON:
        print('OFF.')
    timer1.deinit()
    Led.value(LED_OFF)    
    print("Stop blinking")
     
def RandomDelay(min, max):
    return min + (max - min)*random.random()

# Execute tasks that require random time while blinking the LED


print('LED should blink at constant rate for next {} seconds.'.format(int(RUNTIME/1000)))

start_time = ticks_ms()    # overall timer
StartLedBlinking()

while True:
  if ticks_ms() - start_time > RUNTIME:
      break
  task_delay = int(RandomDelay(3*PERIOD/4, 4*PERIOD))
  sleep_ms(task_delay)
  print('Did something requiring {} milliseconds'.format(task_delay))

print('Done.')
StopLedBlinking()

Led.value(LED_OFF)
