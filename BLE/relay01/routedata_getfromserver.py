import socket
import ubinascii
import urequests
import time
import json
import pickle
from machine import Pin, Timer
import micropython,time
import _thread
import machine
import utime
import ure
green_led = None
route = None
true = False
data = " "

green_pin = 14
green_led = machine.Pin(green_pin, machine.Pin.OUT)
    
def led():
    global  green_led, true
    while true is False:
        green_led.on()
        utime.sleep(0.5)
        green_led.off()
        utime.sleep(0.5)
    _thread.exit()
    return true


def get():
    global green_led, route,true
    
    url = "http://192.168.156.229:5000/send_to_esp"
    #urequests.head(url)
    print("test")
    
    sendData = {"sign": "test"}
    print(sendData)
    header = {'Content-Type': 'application/json'}
    try:
        res = urequests.post(url, data=json.dumps(sendData),headers=header)
        print("サーバからのステータスコード：", res.status_code)
        #print(res)
        resp = res.json()
        
        resp = resp["routedata"]    
        recv = bytes(resp, "utf-8")
        recv = recv.replace(b',', b'\n')
        route = str(recv, "utf-8")
        print(route)
        return route
    except:
        print('失敗しました')
        ture = True
    
    finally:
        true = True
        print('終了です')
        #_thread.exit()

if __name__ == "__main__":
    get()
