# customboot.py
# Connects to a local Wi-Fi network or if failing that
# starts a Wi-Fi access point. In either case, an FTP
# server is also started.
#
# Imports a secrets.py script with the Wi-Fi credentials
# and other parameters.
#
# Either remove the original boot.py and rename this
# script boot.py or add
# import customboot.py
# in boot.py

from time import sleep
from network import WLAN, STA_IF, AP_IF, AUTH_OPEN, AUTH_WPA2_PSK_AES
from machine import reset
from w600 import run_ftpserver
from secrets import *

print("")
print("W600-PICO Boot")
print("")

def startFTP():
  run_ftpserver(port=FTP_PORT,username=FTP_USER,password=FTP_PSWD)
  print("FTP server on port {}, username is {}, password is {}".format(FTP_PORT, FTP_USER, FTP_PSWD))
    
wlan = WLAN(STA_IF)

for attempt in range(CONNECT_TRIES):
  wlan.active(True)
  print('Connect attempt {}...'.format(attempt+1))
  wlan.connect(STA_SSID, STA_PSWD)
  for i in range(CONNECT_TIMEOUT):
    if wlan.isconnected():
      print("Success on attempt {} after {} seconds".format(attempt+1, i))
      break # from inner loop
    else:
      sleep(1)
  if wlan.isconnected():
    break # from outer loop
  else:
    wlan.active(False)
    
if not wlan.isconnected():
  print("Could not connect to {}".format(STA_SSID))   
  ap_if = WLAN(AP_IF)
  ap_if.active(True)
  if AP_PSWD is None:
    ap_if.config(essid=AP_SSID,authmode=AUTH_OPEN,channel=11)
  else:
    ap_if.config(essid=AP_SSID,password=AP_PSWD,authmode=AUTH_WPA2_PSK_AES,channel=11)
  print("Access point {} started at IP 192.168.43.1".format(AP_SSID))
  startFTP()
  sleep(AP_UP_TIME)
  ap_if.active(False)
  print("Restarting")
  reset()

# wlan connected
if not STA_FIXED_IP == "0.0.0.0":
  wlan.ifconfig((STA_FIXED_IP, STA_SUBNET, STA_GATEWAY, STA_DNS))
print("Connected to {}, IP is {}".format(STA_SSID, wlan.ifconfig()[0]))
startFTP()
