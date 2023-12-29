import _peripheral
import _central
import makeroute
import maketabledata
from machine import I2C,Pin
#from vl53l1x import VL53L1X
import machine
import ubinascii
import json

red_pin = 13
red_led = machine.Pin(red_pin, machine.Pin.OUT)
green_pin = 14
green_led = machine.Pin(green_pin, machine.Pin.OUT)
blue_pin = 15

blue_led = machine.Pin(blue_pin, machine.Pin.OUT)

fn = 'info/DN05.json'

class ManagementRoute():
    # センサデバイスの行う動作を纏めたクラス.
    # Manegmentクラスを定義して経路データの送受信と書き込み(，確認)を行う各モジュールを呼び出すdef関数を定義する．
    
    def _RoutedataCatch(self, fn, blue_led, mode):
        #RD = routedata_central.Centr()
        RD = _central.centr(fn, blue_led, mode)
        return RD
    
    def _RoutedataSend(self, fn, data, blue_led, mode,time): # 経路データの送信
        connection = _peripheral.periph(fn, data, blue_led, mode, time)
        return connection
        
    def _RoutedataGet(self,fn, blue_led, mode): # 経路表作成用のデータ取得
        #routedata = routeget_central.Centr(blue_led)
        routedata = _central.centr(fn, blue_led, mode)
        #print(routedata)
        return routedata

    def _MakeTableData(self, fn, all_data,orthopedy_data):
        maketabledata.MakeData(fn, all_data,orthopedy_data)

    def _MakeRouteTable(self,fntxt,fnjson): # 経路表作成
        makeroute._routemake(fntxt,fnjson)
        
    def _RoutedataBack(self, fn, data, blue_led, mode,time):
        connection = _peripheral.periph(fn, data, blue_led, mode, time)
        return connection

def MGRoute(fn, Pmode_change,Cmode_change,fntxt1,fntxt2, fntxt3, fnjson1, condition1):
    mg = ManagementRoute()
    
    OPEN = open(fn, 'r')
    LOAD = json.load(OPEN)
    dev_name = str(LOAD["device_number"])
    
    if condition1 is 0: #senser間通信
        #Cmode:0
        RD = mg._RoutedataCatch(fn, blue_led, Cmode_change)
        
        Cmode_change += 1
        
        data = str(RD) + "_" + dev_name
        

        #Pmode:0
        data = mg._RoutedataSend(fn, data, blue_led, Pmode_change, 20)
        
        Pmode_change += 1
        
        SSroute = mg._RoutedataGet(fn, blue_led, Cmode_change)
        
        Cmode_change += 1
        
        data = SSroute
        
        data = mg._RoutedataBack(fn, data, blue_led, Pmode_change, 20)
        
        Pmode_change += 1
        
        print("完了")
        
        
    if condition1 is 1: #senser-server間
        
        print("senser-server間経路")
        #Cmode:3
        RD = mg._RoutedataCatch(fn, blue_led, Cmode_change)
        
        Cmode_change += 1
        
        data = str(RD) + "_" + dev_name
        
        #Pmode:3
        data = mg._RoutedataSend(fn, data, blue_led, Pmode_change, 25)
        
        Pmode_change += 1
        
        print("testtest")
        
        #Cmode:4
        route = mg._RoutedataGet(fn, blue_led, Cmode_change)
        
        Cmode_change += 1
        
        #Pmode:4
        dt = mg._RoutedataBack(fn, route, blue_led, Pmode_change, 20)
        
        Pmode_change += 1
        
        all_data = fntxt1
        orthopedy_data = fntxt2
        
        #mg._MakeTableData(fn, all_data, orthopedy_data)
        
        fntxt = fntxt3
        fnjson = fnjson1

        #mg._MakeRouteTable(fntxt, fnjson)
    
    print(Pmode_change)
    print(Cmode_change)
    return Pmode_change, Cmode_change
    
    #except:
    #    print("途中終了")


if __name__ == "__main__":
    Pmode_change = 3
    Cmode_change = 3
    fn = 'info/DN05.json'
    fntxt1 = "data/routetabledata.txt"
    fntxt2 = 'data/makeroute_data.txt'
    fntxt3 = 'data/makeroute_data.txt'
    fnjson1 = 'data/routeinfo.json'
    #print(ubinascii.hexlify('tosenser'))
    condition1 = 1
    MGRoute(fn, Pmode_change, Cmode_change, fntxt1, fntxt2, fntxt3, fnjson1, condition1)
