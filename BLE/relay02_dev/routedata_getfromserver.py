import socket
import ubinascii
import urequests
import time
import json
import pickle
from machine import Pin, Timer
import micropython,time
import _thread

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
    green_led.off()
    return true


def get():
    global green_led, route,true
    
    #url = "http://192.168.193.73:5000/send_to_esp"
    url = "http://192.168.193.229:80/send_to_esp"
    
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
        recv = pickle.loads(recv)
        print(type(recv))
        
        if b'\x80\x04]\x94.' in recv:
            print("空のlistを受け取りました．")
        else:
            recv = recv.replace(b'\x80\x04\x95\x1d', b'')
            recv = recv.replace(b'\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c',b'')
            recv = recv.replace(b'\t', b'')
            recv = recv.replace(b'\x94\x8c', b'\n')
            recv = recv.replace(b'\x94e.', b'')
            recv = recv.replace(b'\x80\x04\x95)', b'')
            recv = recv.replace(b'\x0b',b'')
            recv = recv.replace(b'\x80\x04\x957', b'')
            recv = recv.replace(b'\x80\x04\x95\x19\x07', b'')
            recv = recv.replace(b'\x07', b'')
            print(recv)
            route = str(recv,'utf-8')
            print(route)
            print(type(route))
            return route
    except:
        print('失敗しました')
        ture = True
    
    finally:
        true = True
        print('終了です')

def Thread():
    data = _thread.start_new_thread(get,())
    _thread.start_new_thread(led,())
    _thread.exit()
    return data

if __name__ == "__main__":
    Thread()
