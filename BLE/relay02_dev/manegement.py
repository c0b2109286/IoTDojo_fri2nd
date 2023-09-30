import routedata_sendtoserver2
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

class Management():
    
    def _RoutedataGet(self,List):
        get = routedata_central2.Centr(List)
        return get
        
    def _RoutedataSendtoServer(self,senddata):
        routedata_sendtoserver2.send(senddata)
        
    def _RoutedataSendtoServer2(self,senddata):
        distance_sendtoserver.send(senddata)
    
    #実際に受け取るときには必要
    def _RouteGetFromServer(self):
        GS = routedata_getfromserver1.get()
        return GS
        
    #def _RoutedataWrite(self, data):
    #    with open('data/routeinfo.txt','w', encoding="utf-8")as f:
    #        print(data)
    #        #print(type(data))
    #        f.write(data)
    #        f.close
            
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
    print(ubinascii.hexlify('esp32'))
    print(ubinascii.hexlify('toserver'))
    print(ubinascii.hexlify('todevice'))
    
    mg = Management()
    
    #connection_list = []
    
    #for i in range(2):
    #for i in range(1):
        #routedata = "5_2_1_2"
        #routedata = mg._RoutedataGet(connection_list)
        
        #jf_open = open('info/DN01.json', 'r')
        #jf_load = json.load(jf_open)
        #gapname = jf_load["device_number"]

        #route = routedata + '_' + str(gapname)
        #print(route)
        #print(len(route))
        #if len(route) is 3:
        #    hop = len(route) - 2
        #if len(route) is 5:
        #    hop = len(route) - 3
        #if len(route) is 7:
        #    hop = len(route) -4
        #if len(route) is 9:
        #    hop = len(route) -5

        #senddata = route + '_' + str(hop)
        #print(senddata)
        
        #response = mg._RoutedataSendtoServer(senddata)
        #time.sleep_ms(1000)
    
    senser1 = 5 
    stop = str(senser1) + "_" + "0"
    responce = mg._RoutedataSendtoServer2(stop)
    getroutedata = getroutedata.replace(',','\n')
    
    #mg._RoutedataWrite(getroutedata)
    
    #mg._SendRouteForDevice(getroutedata)
    
    #route_data = mg._RoutedataCatch()
    #mg._MakeRouteTable()
    
    distance = mg.SenserdataGet()
    
    dist = distance.replace(" ",'')
    dist = distance.replace('\x00','')
    print(dist)
    print(type(dist))
    
    mg.SenserdataSend(distance)
