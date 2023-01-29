# webserver3 for W600-PICO running MicroPython 1.19 - display blocking problem with simple web server

from network import WLAN, STA_IF 
from machine import Pin, Timer, PWM
from time import sleep_ms
import socket
import webresponses

wlan = WLAN(STA_IF)
if not wlan.isconnected():
    import customboot


print()
print('Executing webserver3.py')
print('-----------------------')
print()

TEST_INTERRUPT    = True
TEST_PWM          = False
SHOW_FULL_REQUEST = False
PERIOD            = 250    # flash on/off time
LED_ON            = 0      # LOW turns the built in LED ON
LED_OFF           = 1      # HIGH turns the built in LED OFF


# Built in blue LED connected to pin labeled PA0 on the board
Led = Pin(Pin.PA_00, Pin.OUT)

Status = LED_OFF

def SetLed(value):
  global Status
  Led.value(Status)
  Status = 1-value  # inverse logic of built in LED
  
# Ensure the built in LED is off to start (it should be after reset)
SetLed(LED_OFF)

# Create timer instance that will toggle the built in LED
timer1 = Timer(1)

# Global variable for PWM channel
pwm0 = None

# timer1 callback function
def LedToggle(t):
    lv = 1 - Led.value()
    Led.value(lv)

def StartLedBlinking():
    print("Start blinking LED")
    # inititate a periodic timer which will exectute LedToggle after PERIOD ms
    if TEST_PWM:
      global pwm0  
      pwm0 = PWM(Pin(Pin.PA_00), channel=0, freq=4, duty=128)
    else:
      global timer1  
      timer1.init(period=PERIOD, mode=Timer.PERIODIC, callback=LedToggle)


def StopLedBlinking():
    if TEST_PWM:
      global pwm0  
      pwm0.deinit()  
    else:
      global timer1
      timer1.deinit()
 
    Led.value(LED_OFF)    
    print("Stop blinking")

BUTTON_PIN = Pin.PA_01

interrupt_flag = 0

def pinISR(pin):
  global interrupt_flag
  interrupt_flag += 1
  print('interrupt {}'.format(interrupt_flag))
  
button_one = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
button_one.irq(trigger=Pin.IRQ_FALLING, handler=pinISR)

if TEST_PWM:
  means = 'PWM'
else:
  means = 'Timer'  

print('Test concurrency of interrupts, {}, and socket'.format(means))
StartLedBlinking()
sleep_ms(15000)   # blink steadily for 15 seconds before starting web server

wlan = WLAN(STA_IF)
if wlan.isconnected():
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binding to all interfaces - server will be accessible to other hosts!   
    s.bind(('0.0.0.0', 80))
    s.listen(3)
    print('Web server started at http://' + wlan.ifconfig()[0])
    print('Click on Quit button to stop the web server')
    
    counter = 0
    while True:
        conn, addr = s.accept()
        print("Connection from client", addr)
        
        # MicroPython socket objects support stream interface directly

        req = conn.readline()
        req = str(req)
        if SHOW_FULL_REQUEST:
            print("Request:")
            print(req)
            while True:
              h = conn.readline()
              if h == b"" or h == b"\r\n":
                 break
              print(h)
        else:
            print("Request", req)  
        if req.find('/quit ') == 6:
          reply  = 1  # quit          
        elif req.find('/?led=toggle ') == 6:
          SetLed(Status) # toggle led
          reply = 0      #  show index.html
        elif req.find('/ ') == 6:
          reply = 0      # show index.html
        else:
          reply = -1     # not found error
         
        #print('reply', reply)
        
        rh1, rh2, rh3 = webresponses.HttpResponseHeader(reply < 0)
        conn.write(rh1)
        if reply < 1:
          conn.write(rh2+rh3+webresponses.HttpPage(reply < 0, Status))
        conn.close()          
        if reply == 1:
          print('Closing web server')  
          break  
        print()                       
        
else: #wlan not connected
    print('Not connected... exiting to REPL')

sleep_ms(10000)   # blink steadily for 10 seconds before continuing
StopLedBlinking()


print('Try running again but setting TEST_PWM =', not TEST_PWM)

print('Done')
