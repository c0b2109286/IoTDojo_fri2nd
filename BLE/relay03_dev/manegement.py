import routedata_peripheral
import routedata_central
import routeget_central
import senddistance_central
import senddistance_peripheral
import makeroute
import maketabledata
#import get
import ubinascii

#with open("data/makeroute_data.txt","w",encoding="utf-8")as f:
#    f.write('')
#    f.close()

class Management():
    # センサデバイスの行う動作を纏めたクラス.
    # Manegmentクラスを定義して経路データの送受信と書き込み(，確認)を行う各モジュールを呼び出す関数を定義する．
    
    def _RoutedataCatch(self):
        RD = routedata_central.Centr()
        return RD
    
    def _RoutedataSend(self ,to ,data): # 経路データの送信
        routedata_peripheral.periph(to, data)
        
    def _RoutedataGet(self): # 経路表作成用のデータ取得
        routedata = routeget_central.Centr()
        #print(routedata)
        return routedata
    
    def _Maketabledata(self):
        maketabledata.MakeTableData()

    def _MakeRouteTable(self): # 経路表作成
        makeroute._routemake()
        
    #def getdistance(self): # 距離データの取得
    #    distance = get.distance()
    #    print("#####")
    #    print(distance) #ここで絶対にstrにしておく
    #    print(type(distance))
    #    distance = str(distance)
    #    print(type(distance))
    #    return distance
    
    def SenserdataCatch(self):
        Dist = senddistance_central.Centr()
        return Dist
        
    def SenserdataSend(self,distance): # 作成した経路表に基づく距離データの送信
        senddistance_peripheral.periph(distance,20)

if __name__ == "__main__":
    print(ubinascii.hexlify('toserver'))
    print(ubinascii.hexlify('esp32_relay3'))
    mg = Management()
    #RD = mg._RoutedataCatch()
    #data = mg._RoutedataSend(10,RD)
    
    #route = mg._RoutedataGet()
    
    mg._Maketabledata()
    mg._MakeRouteTable()
    #distance = mg.getdistance()
    distance = mg.SenserdataCatch()
    mg.SenserdataSend(distance)

