# webserver for W600-PICO running MicroPython 1.19 - simple web server
#
# References:
#
# - Beginners Guide to MicroPython: Network & Web Server Examples
#   @ https://siytek.com/micropython-networking-web-server/#Testing-the-ESP8266-web-server
#   by Siytek 2022-08-15
#
# - ESP32/ESP8266 MicroPython Web Server – Control Outputs
#   @ https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
#   by RANDOM NERD TUTORIALS
#
#
from network import WLAN, STA_IF 
from machine import Pin
import socket
import webresponses

print()
print('Executing webserver.py')
print('----------------------')
print()

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
    while True:
      conn, addr = s.accept()
      print()
      print('Client connection from {}'.format(addr))
      request = conn.recv(1024)
      request = str(request)
      print('Resquest {}...'.format(request[0:31]))
      if request.find('/quit ') == 6:
        reply  = 1  # quit          
      elif request.find('/?led=toggle ') == 6:
        SetLed(Status) # toggle led
        reply = 0      #  show index.html
      elif request.find('/ ') == 6:
        reply = 0      # show index.html
      else:
        reply = -1     # not found error
      rh1, rh2, rh3 = webresponses.HttpResponseHeader(reply < 0)
      #print('rh1: {}, rh2: {}, rh3: {}'.format(rh1, rh2, rh3))
      conn.send(rh1)
      if reply < 1:
        conn.send(rh2)
        conn.send(rh3)
        conn.sendall(webresponses.HttpPage(reply < 0, Status))
      conn.close()
      if reply == 1:
        break  

else: #wlan not connected
    print('Not connected... exiting to REPL')

