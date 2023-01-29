from os import uname

print()
print('===========')
print('= demo.py =')
print('===========')
print()
print("os.uname:")
print(uname())
print()
print("Ctrl-C to halt demonstration")

# connect to network
import customboot

# network connection not needed
import blink
import blink2
import blink3
import blink4
import pollbutton
import pollbutton2
import intrbutton

# network connection needed
import webserver
import mqtttest
import wifiswitch

print()
print()
print('Back to REPL')
print()