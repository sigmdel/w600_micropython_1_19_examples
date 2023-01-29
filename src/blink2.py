# Blink2 for W600-PICO running MicroPython 1.19 - multitasking with ticks

from machine import Pin
from time import sleep_ms, ticks_ms
import random

print()
print('Executing blink2.py')
print('-------------------')
print()

RUNTIME = 15000 # flash for 15 seconds
PERIOD = 250    # flash on/off time
LED_ON = 0  # LOW turns the built in LED ON
LED_OFF = 1 # HIGH turns the built in LED OFF

# Built in blue LED connected to pin labeled PA0 on the board
Led = Pin(Pin.PA_00, Pin.OUT)

# Ensure the built in LED is off to start (it should be after reset)
Led.value(LED_OFF)

def LedToggle():
    lv = 1 - Led.value()
    Led.value(lv)

def RandomDelay(min, max):
    return min + (max - min)*random.random()

start_time = ticks_ms()    # overall timer
led_ticks = ticks_ms()

# Execute tasks that require random time and blink LED at same time

print('LED should blink at constant rate for next {} seconds.'.format(int(RUNTIME/1000)))
while True:
  if ticks_ms() - start_time > RUNTIME:
      break
  if ticks_ms() - led_ticks > PERIOD:
      LedToggle()
      led_ticks = ticks_ms()
  task_delay = int(RandomDelay(PERIOD/4, 3*PERIOD/4))
  sleep_ms(task_delay)
  print('Did something requiring {} milliseconds'.format(task_delay))

Led.value(LED_OFF)
start_time = ticks_ms()    # overall timer
led_ticks = ticks_ms()

print('LED should blink at variable rate for next {} seconds.'.format(int(RUNTIME/1000)))
while True:
  if ticks_ms() - start_time > RUNTIME:
      break
  if ticks_ms() - led_ticks > PERIOD:
      LedToggle()
      led_ticks = ticks_ms()
  task_delay = int(RandomDelay(3*PERIOD/4, 4*PERIOD))
  sleep_ms(task_delay)
  print('Did something requiring {} milliseconds'.format(task_delay))

Led.value(LED_OFF)
print('Done.')

