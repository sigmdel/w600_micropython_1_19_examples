# intrbutton for W600-PICO running MicroPython 1.19 monitoring push button with interrupts

from machine import Pin    # builtin
from time import ticks_ms  # builtin

print()
print('Executing intrbutton.py')
print('-----------------------')
print()

BUTTON_PIN = Pin.PA_01

interrupt_flag = 0

def pinISR(pin):
  global interrupt_flag
  interrupt_flag += 1

button_one = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
button_one.irq(trigger=Pin.IRQ_FALLING, handler=pinISR)

# Run for milli seconds.
RUNTIME = 15000
starttick = ticks_ms()

print('Setup completed, will run for {} seconds. Start pressing button.'.format(RUNTIME/1000))

while ticks_ms() - starttick < RUNTIME:
  if interrupt_flag:
      print("Button pressed {} times".format(interrupt_flag))
      interrupt_flag = 0

# fall back into REPL
print("Done.")
