import _peripheral
import _central
import makeroute
import maketabledata
from machine import I2C,Pin
from vl53l1x import VL53L1X
import machine
import ujson
import utime

red_pin = 13
red_led = machine.Pin(red_pin, machine.Pin.OUT)
green_pin = 14
green_led = machine.Pin(green_pin, machine.Pin.OUT)
blue_pin = 15
blue_led = machine.Pin(blue_pin, machine.Pin.OUT)

class ManagementRoute():
    # センサデバイスの行う動作を纏めたクラス.
    # Manegmentクラスを定義して経路データの送受信と書き込み(，確認)を行う各モジュールを呼び出す関数を定義する．
    
    def _RoutedataSend(self, fn, distance, blue_led, mode,time): # 経路データの送信
        connection = _peripheral.periph(fn, distance, blue_led, mode, time)
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

def MGRoute(fn, Pmode_change,Cmode_change, condition1):
    mg = ManagementRoute()
    connect =0
    timeout = 20
    print("`````````")
    print(Pmode_change)
    print(Cmode_change)
    print("`````````")
    
    OPEN = open(fn, 'r')
    LOAD = ujson.load(OPEN)
    dev_name = str(LOAD['device_number'])
    
    
    if condition1 is 0: #中継器役割 Pmode:0, Cmode:0
        
        #Cmode:0
        data = mg._RoutedataGet(fn, blue_led, Cmode_change) #senser-senser route
        
        Cmode_change += 1
        
        routedata = str(data) + '_' + str(dev_name) + "_1_1"
        
        #Pmode:0
        mg._RoutedataSend(fn, routedata, blue_led, Pmode_change, timeout)
        
        Pmode_change += 1
        
        fntxt = 'data/SenserRoutedata.txt'
        fnjson = 'data/SenserRouteinfo.json'

        #mg._MakeRouteTable(fntxt, fnjson)
        
        #Pmode:1
        #Cmode:1
        
    if condition1 is 1:#センサー役割 Pmode:1, Cmode:2
        
        #Pmode:1
        for i in range(2):
            print("tsts")
            data = mg._RoutedataSend(fn, dev_name, blue_led, Pmode_change, timeout)
            
            print(Pmode_change)
            connect += data
            
        print(connect)
        
        Pmode_change += 1
        
        utime.sleep(10)
        
        Cmode_change = 2
        #Cmode:2
        
        for i in range(2):
            routedata = mg._RoutedataGet(fn, blue_led,Cmode_change)
        
        Cmode_change += 1
                
        all_data = "data/routetabledata.txt"
        orthopedy_data = 'data/makeroute_data.txt'
        
        #mg._MakeTableData(fn, all_data, orthopedy_data)
        
        fntxt = 'data/makeroute_data.txt'
        fnjson = 'data/routeinfo.json'

        #mg._MakeRouteTable(fntxt, fnjson)
        
        #Pmode:2
        #Cmode:3
            
    #except:
    print("強制終了")
    #Pmode_change += 1
    #Cmode_change += 1    
    #finally:
    #中継器:P1,C1
    #センサ:P2,C:3
    print(Pmode_change)
    print(Cmode_change)
    return Pmode_change, Cmode_change

if __name__ == "__main__":
    fn = 'info/SN02.json'   
    Pmode_change = 1
    Cmode_change = 2
    condition1 = 1
    MGRoute(fn, Pmode_change, Cmode_change, condition1)
