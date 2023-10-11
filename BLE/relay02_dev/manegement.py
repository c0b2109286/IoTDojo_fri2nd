import routedata_sendtoserver2
#import routedata_sendtoserver
import routedata_central2
import senddistance_central2
import distance_sendtoserver2
import distance_sendtoserver
#import senddistance_peripheral
import makeroute
import ubinascii
import json
import routedata_getfromserver1

import routesendtodevice_peripheral1
import time
from machine import Pin, Timer
import micropython,time
import _thread
from machine import Pin, Timer
import micropython,time


class Management():
    
    def _RoutedataGet(self,List):
        get = routedata_central2.Centr(List)
        return get
        
    def _RoutedataSendtoServer(self,senddata):
        routedata_sendtoserver2.send(senddata)
        
    def _RoutedataSendtoServer2(self,senddata):
        distance_sendtoserver2.send(senddata)
    
    #実際に受け取るときには必要
    def _RouteGetFromServer(self):
        GS = routedata_getfromserver1.get()
        return GS
            
    def _SendRouteForDevice(self,data):
        routesendtodevice_peripheral1.periph(data)
        

    def _MakeRouteTable(self,data):
        #with open("routedata_test.txt",'w',encoding="utf-8")as f:
        #    f.writelines(data)
        #f.close()
        makeroute._routemake()
        
    def SenserdataGet(self):
        distance = senddistance_central2.Centr()
        return distance
        
    def SenserdataSend(self,distance):
        distance_sendtoserver2.send(distance)
        
    
if __name__ == "__main__":
    mg = Management()
    connection_list = []
    lsls = True
    mess = None
    green_led = None
    #TM = 10000
    
    micropython.alloc_emergency_exception_buf(100)
    oneShotTimer = Timer(0)
    
    def ROUTECODE():
        global mess,lsls,green_led
        while mess is None:
            if lsls is True:
                
                routedata = mg._RoutedataGet(connection_list)
                
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

                senddata = route + '_' + str(hop)
                print(senddata)
                
                green_pin = 14
                green_led = machine.Pin(green_pin, machine.Pin.OUT)
                try:
                    green_led.on()
                    response = mg._RoutedataSendtoServer(senddata)
                    #time.sleep_ms(1000)
                    green_led.off()
                except:
                    green_led.off()
                finally:
                    green_led.off()
                time.sleep_ms(1000)


    def Return(timer,message="時間が経ちました"):
        global mess
        mess = message
        print(mess)
    
    def TIMER(TM=10000):
        global mess
        oneShotTimer.init(mode=Timer.ONE_SHOT, period=TM, callback=Return)
        
    print ("タイマーを開始します")
    _thread.start_new_thread(TIMER,())
    _thread.start_new_thread(ROUTECODE,())
    
    
    mainLoop=0
    #while mainLoop < 10:
    while mess is None:
        mainLoop += 1
        print("MAIN:", mainLoop)
        time.sleep_ms(1000)
    lsls = False
    green_led.off()
    
    #senser1 = "5_0_0"
    #stop = str(senser1) + "_" + "0"
    #responce = mg._RoutedataSendtoServer2(stop)
    
    routetabledata = mg._RouteGetFromServer()
    
    with open('data/routetabledata.txt','w',encoding='utf-8')as f:
        f.write(routetabledata)
        f.close()
    
    mg._SendRouteForDevice(routetabledata)
    
    #mg._MakeRouteTable()
    
    #distance = mg.SenserdataGet()
    
    #dist = distance.replace(" ",'')
    #dist = distance.replace('\x00','')
    #print(dist)
    #print(type(dist))
    
    #mg.SenserdataSend(distance)
