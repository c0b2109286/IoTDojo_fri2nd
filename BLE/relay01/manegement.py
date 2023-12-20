import _peripheral
import _central
import distance_sendtoserver
import routedata_sendtoserver
import routedata_getfromserver
import makeroute
import ubinascii
import json
import machine
import time
from machine import Pin, Timer
import micropython,time
import _thread

red_pin = 13
red_led = machine.Pin(red_pin, machine.Pin.OUT)
green_pin = 14
green_led = machine.Pin(green_pin, machine.Pin.OUT)
blue_pin = 15
blue_led = machine.Pin(blue_pin, machine.Pin.OUT)

fn = 'info/DN01.json'
url = 'http://192.168.60.73:5000'

class Management():
    
    def _LEDRESET(self):
        global red_led, green_led, blue_led
        red_led.off()
        green_led.off()
        blue_led.off()
        
    
    def _RoutedataGet(self, fn, _led, mode):
        get = _central.Centr(fn, _led, mode)
        return get
        
    def _RoutedataSendtoServer(self,senddata, url):
        routedata_sendtoserver.send(senddata, url)
        
    #実際に受け取るときには必要
    def _RouteGetFromServer(self, url):
        GS = routedata_getfromserver.get(url)
        return GS
            
    def _SendRouteForDevice(self, fn, routedata, _led, mode, timeout):
        _peripheral.periph(fn, routedata, _led, mode, timeout)
        

    def _MakeRouteTable(self,data):
        makeroute._routemake()
        
    def SenserdataGet(self, fn, _led, mode):
        distance = _central.Centr(fn, _led, mode)
        return distance
        
    def SenserdataSend(self,distance, url):
        distance_sendtoserver.send(distance, url)
        
    
if __name__ == "__main__":
    mg = Management()
    connection_list = []
    lsls = True
    mess = None
    
    Pmode_change = 0
    Cmode_change = 0
    
    micropython.alloc_emergency_exception_buf(100)
    oneShotTimer = Timer(0)
    
    def ROUTECODE():
        global mess, lsls, red_led, Cmode_change
        #while mess is None:
        for i in range(2):
            
            if lsls is False:
                print("終了です")
                break
            
            routedata = mg._RoutedataGet(fn, red_led, Cmode_change)
            
            print("受信中")
            
            #_thread.start_new_thread(thread1_1, ())
            #_thread.start_new_thread(thread1_2, ())
        
            jf_open = open('info/DN01.json', 'r')
            jf_load = json.load(jf_open)
            gapname = jf_load["device_number"]
            
            print("+*+*+*+*+*+*+*")
            print(routedata)

            route = routedata + '_' + str(gapname)
        
            print(route)
            print(len(route))
            if len(route) is 3:
                hop = len(route) - 2
            if len(route) is 5:
                hop = len(route) - 3
            if len(route) is 7:
                hop = len(route) -4
            if len(route) is 9:
                hop = len(route) -5

            senddata = str(route) + '_' + str(hop)
            print(senddata)
        
            response = mg._RoutedataSendtoServer(senddata, url)
            
            Cmode_change += 1
            
    def Return(timer,message="時間が経ちました"):
        global mess
        mess = message
        print(mess)
    
    def TIMER(TM=10000): #10秒のtimer
        global mess
        oneShotTimer.init(mode=Timer.ONE_SHOT, period=TM, callback=Return)
        #_thread.exit()
        
    def TIMER1(TM=15000): #10秒のtimer
        global mess
        oneShotTimer.init(mode=Timer.ONE_SHOT, period=TM, callback=Return)
        
    
    print ("タイマーを開始します")
    _thread.start_new_thread(TIMER,())
    _thread.start_new_thread(ROUTECODE,())
        
    mainLoop=0
        #while mainLoop < 10:
    #while mess is None:
    for i in range(10): 
        mainLoop += 1
        print("MAIN:", mainLoop)
        time.sleep_ms(1000)
        i += 1
        if mainLoop is 10:
            lsls = True
            green_led.off()
        
    senser1 = "3_0_0"
    stop = str(senser1) + "_" + "0"
    responce = mg._RoutedataSendtoServer(stop, url)
    
    print("print")
    routetabledata = mg._RouteGetFromServer(url)
    
    for i in range(2):
        mg._SendRouteForDevice(fn, routetabledata, blue_led, Pmode_change, 20)
        Pmode_change += 1
        
    #Cmode_change += 1 #Cmod:1
    
    time.sleep(30)
    
    print ("タイマーを開始します")
    _thread.start_new_thread(TIMER1,())
    _thread.start_new_thread(ROUTECODE,())
    
    
    mainLoop=0
        #while mainLoop < 10:
    #while mess is None:
    for i in range(15): 
        mainLoop += 1
        print("MAIN:", mainLoop)
        time.sleep_ms(1000)
        i += 1
        if mainLoop is 15:
            lsls = True
            green_led.off()
    
    
    senser1 = "7_0_0"
    stop = str(senser1) + "_" + "0"
    responce = mg._RoutedataSendtoServer(stop, url)
    
    time.sleep(3)
    
    print("print")
    routetabledata = mg._RouteGetFromServer(url)
    
    print(routetabledata)
    print(type(routetabledata))
    
    mg._SendRouteForDevice(fn, routetabledata, blue_led, Pmode_change, 30)
    Pmode_change += 1 #Pmode:3
    
    
    utime.sleep(10)
    print("distance")
    
    Cmode_change = 5 #Cmod:2
        
    for i in range(3):
        distance = mg.SenserdataGet(fn, red_led, Cmode_change)
        mg.SenserdataSend(distance, url)
        #Cmode_change += 1
        utime.sleep(10)
    print("end_point")
