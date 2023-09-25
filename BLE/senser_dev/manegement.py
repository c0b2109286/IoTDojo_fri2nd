import routedata_peripheral
import routeget_central
import senddistance_peripheral
import makeroute
import get
import ubinascii

import time
from machine import I2C,Pin
from vl53l1x import VL53L1X

#with open("data/makeroute_data.txt","w",encoding="utf-8")as f:
#    f.write('')
#    f.close()

class Management():
    # センサデバイスの行う動作を纏めたクラス.
    # Manegmentクラスを定義して経路データの送受信と書き込み(，確認)を行う各モジュールを呼び出す関数を定義する．
    
    def _RoutedataSend(self): # 経路データの送信
        connection = routedata_peripheral.periph()
        return connection
        
    def _RoutedataGet(self): # 経路表作成用のデータ取得
        routedata = routeget_central.Centr()
        #print(routedata)
        return routedata

    def _MakeRouteTable(self): # 経路表作成
        makeroute._routemake()
        
    def getdistance(self): # 距離データの取得
        I2C_SCL_PIN = 22  
        I2C_SDA_PIN = 21
        i2c = I2C(scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN))

        distance = get.distance(i2c)
        print("#####")
        print(distance) #ここで絶対にstrにしておく
        print(type(distance))
        distance = str(distance)
        print(type(distance))
        return distance
        
    def SenserdataSend(self,distance): # 作成した経路表に基づく距離データの送信
        senddistance_peripheral.periph(distance,10)

if __name__ == "__main__":
    print(ubinascii.hexlify('toserver'))
    mg = Management()
    #connect = 0
    #for i in range(2):
    #    data = mg._RoutedataSend()
    #    print(data)
    #    connect += data
    #print(connect)
    #utime.sleep_ms(1000)
    #route = mg._RoutedataGet()

    mg._MakeRouteTable()
    distance = mg.getdistance()
    mg.SenserdataSend(distance)
