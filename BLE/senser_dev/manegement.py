import routedata_peripheral
import routeget_central
import senddistance_peripheral
import makeroute
import get

with open("data/makeroute_data.txt","w",encoding="utf-8")as f:
    f.write('')
    f.close()

class Management():
    # センサデバイスの行う動作を纏めたクラス.
    # Manegmentクラスを定義して経路データの送受信と書き込み(，確認)を行う各モジュールを呼び出す関数を定義する．
    
    def _RoutedataSend(self): # 経路データの送信
        routedata_peripheral.periph()
        
    def _RoutedataGet(self): # 経路表作成用のデータ取得
        routedata = routeget_central.Centr()
        #print(routedata)
        return routedata

    def _MakeRouteTable(self): # 経路表作成
        makeroute._routemake()
        
    def getdistance(self): # 距離データの取得
        distance = get.distance()
        print("#####")
        print(distance) #ここで絶対にstrにしておく
        print(type(distance))
        distance = str(distance)
        print(type(distance))
        return distance
        
    def SenserdataSend(self,distance): # 作成した経路表に基づく距離データの送信
        senddistance_peripheral.periph(distance,10)

if __name__ == "__main__":
    mg = Management()
    data = mg._RoutedataSend()
    route = mg._RoutedataGet()
    mg._MakeRouteTable()
    distance = mg.getdistance()
    mg.SenserdataSend(distance)
