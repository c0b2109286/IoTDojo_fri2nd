import _peripheral
import _central
import makeroute
import maketabledata
from machine import I2C,Pin
#from vl53l1x import VL53L1X
import machine
import ubinascii
import ujson
import utime

red_pin = 13
red_led = machine.Pin(red_pin, machine.Pin.OUT)
green_pin = 14
green_led = machine.Pin(green_pin, machine.Pin.OUT)
blue_pin = 15
blue_led = machine.Pin(blue_pin, machine.Pin.OUT)

fn = 'info/DN04.json'

# class that colect the action performed by the senser device
class ManagementRoute():
    # Define functions to call each module that sends, receves, and writes route data
    def _RoutedataCatch(self, fn, blue_led, mode):
        #RD = routedata_central.Centr()
        RD = _central.centr(fn, blue_led, mode)
        return RD
    
    def _RoutedataSend(self, fn, data, blue_led, mode,time): 
        connection = _peripheral.periph(fn, data, blue_led, mode, time)
        return connection
        
    def _RoutedataGet(self,fn, blue_led, mode): 
        #routedata = routeget_central.Centr(blue_led)
        routedata = _central.centr(fn, blue_led, mode)
        #print(routedata)
        return routedata

    def _MakeTableData(self, fn, all_data,orthopedy_data):
        maketabledata.MakeData(fn, all_data,orthopedy_data)

    def _MakeRouteTable(self,fntxt,fnjson): 
        makeroute._routemake(fntxt,fnjson)
        
    def _RoutedataBack(self, fn, data, blue_led, mode,time):
        connection = _peripheral.periph(fn, data, blue_led, mode, time)
        return connection

def MGRoute(fn, Pmode_change,Cmode_change,condition1):
    mg = ManagementRoute()
    
    OPEN = open(fn, 'r')
    LOAD = ujson.load(OPEN)
    dev_name = str(LOAD['device_number'])
    
    if condition1 is 0:
    #mode 0  toserver not senser
        RD = mg._RoutedataCatch(fn, blue_led, Cmode_change)
        
        Cmode_change += 1
        
        data = str(RD) + '_' + dev_name
        
        #mode 0  send to server routedata
        data = mg._RoutedataSend(fn, data, blue_led, Pmode_change, 30)
        
        Pmode_change += 1
        
        print("testtest")
        #print(Cmode_change)
        
        #Cmode 1  for senser  return routedata
        utime.sleep(10)
        route = mg._RoutedataGet(fn, blue_led, Cmode_change)
        Cmode_change += 1
        
        #Pmode 1 for senser  return routedata
        #utime.sleep(5)
        dt = mg._RoutedataBack(fn, route, blue_led, Pmode_change, 20)
        Pmode_change += 1
        
        all_data = "data/routetabledata.txt"
        orthopedy_data = 'data/makeroute_data.txt'
        
        mg._MakeTableData(fn, all_data, orthopedy_data)
        
        fntxt = 'data/makeroute_data.txt'
        fnjson = 'data/routeinfo.json'

        #mg._MakeRouteTable(fntxt, fnjson)
    
    if condition1 is 1:
    #mode 0  toserver not senser
        
        for i in range(2):
            #Cmode:2
            RD = mg._RoutedataCatch(fn, blue_led, Cmode_change)
        
            
            data = str(RD) + '_' + dev_name
            
            #Pmode:2
            data = mg._RoutedataSend(fn, data, blue_led, Pmode_change, 20)
            
            #Pmode_change += 1
            
        Cmode_change += 1
        Pmode_change += 1
        
        print("testtest")
        #print(Cmode_change)
        
        #Cmode:3
        route = mg._RoutedataGet(fn, blue_led, Cmode_change)
        
        Cmode_change += 1
        
        for i in range(2):
            #Pmode:3，4
            dt = mg._RoutedataBack(fn, route, blue_led, Pmode_change, 20)
            Pmode_change += 1
        
        all_data = "data/routetabledata.txt"
        orthopedy_data = 'data/makeroute_data.txt'
        
        mg._MakeTableData(fn, all_data, orthopedy_data)
        
        fntxt = 'data/makeroute_data.txt'
        fnjson = 'data/routeinfo.json'

        #mg._MakeRouteTable(fntxt, fnjson)
    
    print(Pmode_change)
    print(Cmode_change)
    return Pmode_change, Cmode_change


if __name__ == "__main__":
    Pmode_change = 2
    Cmode_change = 2
    fn = 'info/DN04.json'
    condition1 = 1
    MGRoute(fn, Pmode_change, Cmode_change, condition1)
