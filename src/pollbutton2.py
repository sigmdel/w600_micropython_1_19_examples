# pollbutton for W600-PICO running MicroPython 1.19 - monitoring push button by polling from a timer

from Button import Button       # from https://github.com/ubidefeo/MicroPython-Button
from machine import Pin, Timer  # builtin
from time import sleep_ms       # builtin

print()
print('Executing pollbutton2.py')
print('------------------------')
print()

BUTTON_PIN = Pin.PA_01
                     
ACTIVE_LOW = True  # One pole of a normally open push button is connected to the I/O pin,
                   # the other pole is connected to Gnd (O volts). An internal or
                   # external pull up resistor must be in place to keep the I/O pin
                   # high when the push button is not pressed.              

released_count = 0

def button_change(button, event):
  global released_count
  if event == Button.RELEASED:
    released_count += 1
    print('Button {} {}. Count: {}'.format(button, event, released_count))
  else:
    print('Button {} {}.'.format(button, event))

# Create a Button class instance
if ACTIVE_LOW:
  button_one = Button(BUTTON_PIN, True, button_change, internal_pullup = True)
else:
  # WARNING: the W600 does not have internal pull down resistor
  button_one = Button(BUTTON_PIN, False, button_change, internal_pulldown = True) 


# button_one will be updated every 50 ms seconds by timer1
BUTTON_PERIOD = 50 # ms

# Create timer instance that will toggle the built in LED
timer1 = Timer(1)

# timer1 callback function
def ButtonUpdate(t):
    button_one.update()

# function to initialize timer1
def StartButton():
    print("Start checking button state")
    # inititate a periodic timer which will exectute LedToggle after PERIOD ms
    timer1.init(period=BUTTON_PERIOD, mode=Timer.PERIODIC, callback=ButtonUpdate)
    
def StopButton():
    timer1.deinit()

# Run for 30 seconds.
HALF_MINUTES = 1

# Time taken by other tasks
OTHER_TIME = 2500 # ms

LOOPS = int(HALF_MINUTES*30*1000/OTHER_TIME)

print('Setup completed, will run for {} seconds. Start pressing button.'.format(HALF_MINUTES*30))

StartButton()
for i in range(LOOPS):
    sleep_ms(OTHER_TIME) # do other tasks
    print('{} ms task {} of {} completed'.format(OTHER_TIME, i+1, LOOPS))
StopButton()

# fall back into REPL
print("Done.")
