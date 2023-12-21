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

fn = 'info/DN02.json'

class ManagementRoute():
    # Class that collect the action performed by the senser device.
    # Define functions to call each module that sends, receives, and writes route data.
    
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

def MGRoute(fn, Pmode_change,Cmode_change):
    global blue_led, red_led, green_led
    mg = ManagementRoute()
    
    OPEN = open(fn, 'r')
    LOAD = ujson.load(OPEN)
    dev_name = str(LOAD['device_number'])
    
    #Cmode 0  senser1　data catch
    RD = mg._RoutedataCatch(fn, red_led, Cmode_change)

    Cmode_change += 1
    
    data = str(RD) + '_' + dev_name
    
    #Pmode 0  send to server
    data = mg._RoutedataSend(fn, data, blue_led, Pmode_change, 20)
    
    Pmode_change += 1
    
    print("testtest")
    
    utime.sleep(10)
    #Cmode Get returned routedata
    route = mg._RoutedataGet(fn, blue_led, Cmode_change)
    Cmode_change += 1
    print(route)
    
    all_data = "data/routetabledata.txt"
    orthopedy_data = 'data/makeroute_data.txt'
    
    with open(orthopedy_data, 'w')as f:
        f.write(route)
        
    mg._MakeTableData(fn, all_data, orthopedy_data)
    
    #Pmode 1 for senser  return routedata
    #utime.sleep(5)
    
    #with open(orthopedy_data, 'w')as f:
    #    f.write(route)
    
    dt = mg._RoutedataBack(fn, route, blue_led, Pmode_change, 20)
    Pmode_change += 1
    
    #fntxt = 'data/makeroute_data.txt'
    #fnjson = 'data/routeinfo.json'

    #mg._MakeRouteTable(fntxt, fnjson)
    
    
    return Pmode_change, Cmode_change


if __name__ == "__main__":
    Pmode_change = 0
    Cmode_change = 0
    fn = 'info/DN02.json'
    #print(ubinascii.hexlify('tosenser'))
    MGRoute(fn, Pmode_change, Cmode_change)
