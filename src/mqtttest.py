# mqtttest for W600-PICO running MicroPython 1.19, testing subscription in MQTT client
#
# Reference:
#   umqtt.simple example_sub_led.py
#   @ https://github.com/micropython/micropython-lib/blob/master/micropython/umqtt.simple/example_sub_led.py

from network import WLAN, STA_IF 
from machine import Pin
from time import sleep_ms, ticks_ms as ticks
import json
from umqtt.simple import MQTTClient
from mqttdata import *

print()
print('Executing mqtttest.py')
print('---------------------')
print()

# User modifiable parameters
RUNTIME = 2*60*1000      # run demo for 2 minutes
DOMO_IDX = 195           # Index of W600 virtual device

# Constants
LED_PIN = Pin.PA_00  # Built in LED connected to I/O pin PA0
LED_ON  = 0          # LOW turns the built in LED ON
LED_OFF = 1          # HIGH turns the built in LED OFF
SUB_TOPIC = "domoticz/out"    # MQTT topic to which Domoticz publishes messages

wlan = WLAN(STA_IF)
if not wlan.isconnected():
    import customboot

# Built in blue LED connected to pin labeled PA0 on the board
Led = Pin(LED_PIN, Pin.OUT)

Status = LED_OFF

def SetLed(value):
  global Status
  print('SetLed(LED_{})'.format('ON' if (value == LED_ON) else 'OFF'))
  Status = value;
  Led.value(Status)
  
# Ensure the built in LED is off to start (it should be after reset)
SetLed(LED_OFF)

# Create MQTT client using values from mqttdata.py
mc = MQTTClient("umqtttest", MQTT_SERVER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PSWD, keepalive=MQTT_KEEPALIVE)
print('Created MQTT client, server: {}, port: {}'.format(MQTT_SERVER, MQTT_PORT))

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

wlan = WLAN(STA_IF)
if wlan.isconnected():

    print("Starting mqtt client & subscribing to", SUB_TOPIC);
    mc.set_callback(sub_cb)
    mc.connect()
    mc.subscribe(SUB_TOPIC)
    
    print()
    print("This script will run for {} minutes.".format(int(RUNTIME/60000)))
    print("Toggle the LED on/off with the Domoticz virtual switch.")
    
    try:
      while True:
        if ticks() - start_time > RUNTIME:
          break;  
        mc.check_msg()
        sleep_ms(50) # need some delay otherwise this does not work
    finally:    
        mc.disconnect()      


