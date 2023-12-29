import _peripheral
import _central
import routeget_central
import makeroute
import maketabledata
from machine import I2C,Pin
from vl53l1x import VL53L1X
import machine
import time

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

def MGRoute(fn, Pmode_change,Cmode_change,condition1):
    global blue_led, red_led, green_led
    mg = ManagementRoute()
    connect =0
    timeout = 20
    
    try:
        print("condition1 is 0")
        if condition1 is 0: #経路構築
            #Pmode:0
            for i in range(3):
            
                mg._RoutedataSend(fn, "0", blue_led, Pmode_change, timeout)
                
            Pmode_change += 1
            print("kokomade")

            #Cmode:0
            data = mg._RoutedataGet(fn, blue_led,Cmode_change) #senser-senser route
            
            Cmode_change += 1

            fntxt = 'data/SenserRoutedata.txt'
            fnjson = 'data/SenserRouteinfo.json'
            
            #mg._MakeRouteTable(fntxt, fnjson)


            #Cmode:1
            for i in range(2):
                mg._RoutedataGet(fn, blue_led,Cmode_change) #senser-server route
            
            Cmode_change += 1

            all_data = "data/routetabledata.txt"
            orthopedy_data = 'data/makeroute_data.txt'

            #mg._MakeTableData(fn, all_data, orthopedy_data)

            fntxt2 = 'data/makeroute_data.txt'
            fnjson2 = 'data/routeinfo.json'

            #mg._MakeRouteTable(fntxt2, fnjson2)

            
        if condition1 is 1:
            
            #CM:2
            data = mg._RoutedataGet(fn, red_led,Cmode_change)
            
            Cmode_change = data[0]
            routedata = data[1]
            Cmode_change += 1
            
            fntxt = 'data/SenserRoutedata.txt'
            fnjson = 'data/SenserRouteinfo.json'

            #mg._MakeRouteTable(fntxt, fnjson)
            
            
            #PM:2
            mg._RoutedataSend(fn, str(routedata), blue_led, Pmode_change, timeout)
            
            Pmode_change += 1
            
        #PM:1 / CM:2
        #PM:3 / CM:3
        mode = (Pmode_change, Cmode_change)
        print(type(mode))
        
    except:
        print("強制終了")
        if condition1 is 0:
            Pmode_change = 1
            Cmode_change = 2
        elif condition1 is 1:
            Pmode_change = 3
            Cmode_change = 3
            
    finally:
        print(Pmode_change)
        print(Cmode_change)
        red_led.off()
        blue_led.off()
        green_led.off()
        return Pmode_change, Cmode_change

if __name__ == "__main__":
    Pmode_change = 0
    Cmode_change = 0
    fn = 'info/SN01.json'
    condition1 = 0
    MGRoute(fn, Pmode_change, Cmode_change, condition1)
