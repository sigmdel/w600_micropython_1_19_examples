# wifiswitch for W600-PICO running MicroPython 1.19 - basic Wi-Fi switch using MQTT

from network import WLAN, STA_IF 
from machine import Pin
from time import sleep_ms, ticks_ms as ticks
import json
from Button import Button  # from https://github.com/ubidefeo/MicroPython-Button
from umqtt.simple import MQTTClient # https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple
from mqttdata import *

wlan = WLAN(STA_IF)
if not wlan.isconnected():
    import customboot

# Will be connected to the network from here

print()
print('Executing wifiswitch.py')
print('-----------------------')
print()

# User modifiable parameters
RUNTIME = 2*60*1000      # run demo for 2 minutes, 0 to run indefinitely
DOMO_IDX = 195           # Index of W600 virtual device
RELAY_PIN = Pin.PB_12    # I/O pin (PB12) connected to a normally open relay
BUTTON_PIN = Pin.PA_01   # I/O pin (PA1) connected to normally open push button 
BUTTON_ACTIVE_LOW = True # other push button pole connected to ground
LOCAL_CONTROL = True     # The button controls the on board LED and Relay directly and updates Domoticz
                         #  if false the button publishes a message to Domoticz which 
                         #  then replies with an MQTT message and it is this message that 
                         #  will control the LED and relay.

# Constants
LED_PIN   = Pin.PA_00  # Built in LED connected to I/O pin PA0
LED_ON    = 0          # LOW turns the built in LED ON
LED_OFF   = 1          # HIGH turns the built in LED OFF
SUB_TOPIC = "domoticz/out"   # MQTT topic to which Domoticz publishes messages
PUB_TOPIC = "domoticz/in"    # MQTT topic to which Domoticz subscribes


Status = LED_OFF  # Assume Led is off

def SetLed(value):
  global Status
  print('SetLed(LED_{})'.format('ON' if (value == LED_ON) else 'OFF'))
  Led.value(value)    #
  Status = 1-value    # inverse logic of built in LED
  Relay.value(Status) 
  
# Ensure the built in LED is off to start (it should be after reset)
# and that the relay is open
                           
def button_change(button, event):
  global Status
  if event == Button.RELEASED:
    print('Button released, toggle LED')
    Status = 1 - Status; # toggle state
    if LOCAL_CONTROL: 
      SetLed(1-Status)
    publish(Status)  # update Domoticz
  
# Create a Button class instance
if BUTTON_ACTIVE_LOW:
  button_one = Button(BUTTON_PIN, True, button_change, internal_pullup = True)
else:
  print('WARNING: the W600 does not have internal pull down resistor, an external resistor must be in place')
  button_one = Button(BUTTON_PIN, False, button_change, internal_pulldown = True) 

# Built in blue LED connected to pin labeled PA0 on the board
Led = Pin(LED_PIN, Pin.OUT)
Relay = Pin(RELAY_PIN, Pin.OUT)

SetLed(LED_OFF) # assume the relay is open

# Create MQTT client using values from mqttdata.py
mc = MQTTClient("umqtttest", MQTT_SERVER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PSWD, keepalive=MQTT_KEEPALIVE)

def publish(ledstatus):
  global mc
  if LOCAL_CONTROL:
    action = "On" if ledstatus else "Off"
    msg = '{"command": "switchlight", "idx":'+str(DOMO_IDX)+', "switchcmd": "' + action +'" }'
  else:
    action = '1' if ledstatus else '0'   
    msg = '{"command": "udevice", "idx":'+str(DOMO_IDX)+', "nvalue": ' + action + ' }'
  mc.publish(PUB_TOPIC, msg)
  print("Tx: topic {}, payload {}".format(str(PUB_TOPIC), msg))
    
# MQTT callback on received messages on the subscribed topic
def sub_cb(topic, msg):
  json_msg = json.loads(msg)
  if json_msg["idx"] == DOMO_IDX:
    print('Rx: topic {}, payload {}..., idx={}, nvalue={}'.format(topic, msg[0:16], json_msg['idx'], json_msg['nvalue']))
    if json_msg["nvalue"] == 0:
      SetLed(LED_OFF)
    elif json_msg["nvalue"] == 1:
      SetLed(LED_ON)  

start_time = ticks()    # overall timer

print("Starting mqtt client & subscribing to", SUB_TOPIC);
mc.set_callback(sub_cb)
mc.connect()
mc.subscribe(SUB_TOPIC)

print()
if RUNTIME > 0:
  print("This script will run for {} minutes.".format(int(RUNTIME/60000)))
print("Toggle the LED on/off and the relay with the Domoticz virtual switch or the push button.")
 
try:
  while True:
    if RUNTIME > 0 and ticks() - start_time > RUNTIME:
      break;  
    mc.check_msg()
    button_one.update()
    sleep_ms(50) # need some delay otherwise it seems mc.check_msg gets overwhelmed
finally:    
  mc.disconnect()      



