# webserver2 for W600-PICO running MicroPython 1.19 - simple web server using MicroPython optimization

# References:
#
# - httpserver.py
#   @ https://github.com/robert-hh/micropython/blob/w60x/examples/network/http_server.py
#   by Paul Sokolovsky (pfalcon) and Damien George (dpgeorge)

#
from network import WLAN, STA_IF 
from machine import Pin
import socket
import webresponses

wlan = WLAN(STA_IF)
if not wlan.isconnected():
    import customboot

print()
print('Executing webserver2.py')
print('-----------------------')
print()

SHOW_FULL_REQUEST = False

LED_ON  = 0      # LOW turns the built in LED ON
LED_OFF = 1      # HIGH turns the built in LED OFF

# Built in blue LED connected to pin labeled PA0 on the board
Led = Pin(Pin.PA_00, Pin.OUT)

Status = LED_OFF

def SetLed(value):
  global Status
  Led.value(Status)
  Status = 1-value  # inverse logic of built in LED
  
# Ensure the built in LED is off to start (it should be after reset)
SetLed(LED_OFF)

wlan = WLAN(STA_IF)
if wlan.isconnected():
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Binding to all interfaces - server will be accessible to other hosts!   
    s.bind(('0.0.0.0', 80))
    s.listen(3)
    print('Web server started at http://' + wlan.ifconfig()[0])
    print('Click on Quit button to stop the script')
    
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
          break  
        print()          
              
        
else: #wlan not connected
    print('Not connected... exiting to REPL')

