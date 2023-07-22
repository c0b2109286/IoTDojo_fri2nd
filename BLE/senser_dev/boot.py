print(open('./boot.py','rU').read())


SSID_NAME = "name"
SSID_PASS = "pass"

import utime
import network
import machine
from machine import Pin
import webrepl
p2 = Pin(2,Pin.OUT)
red = Pin(13, Pin.OUT)
blue = Pin(4, Pin.OUT)
green = Pin(5, Pin.OUT)

def connect_wifi(ssid, passkey, timeout=10):
    wifi= network.WLAN(network.STA_IF)
    if wifi.isconnected():
        p2.on()
        print('already Connected. connect skip')
        return wifi
    else :
        wifi.active(True)
        count = 0
        while count < 5:
            try:
                wifi.connect(ssid, passkey)
                break
            except:
                utime.sleep(3)
                count += 1
        while not wifi.isconnected() and timeout > 0:
            print('.')
            utime.sleep(1)
            timeout -= 1
    
    if wifi.isconnected():
        p2.on()
        print('Connected')
        webrepl.start(password='1234')
        return wifi
    else:
        print('Connection failed!')
        return ''

machine.freq(240000000)
wifi= connect_wifi(SSID_NAME, SSID_PASS)
