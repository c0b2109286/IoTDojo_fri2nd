import routedata_peripherals1
import routeget_centrals1
import senddistance_peripherals1
import makeroute_s1
import get_s1

def nameinfo():
    dev_name = 8 # デバイス名
    return dev_name
def packetinfo():
    dev_packet = "esp32-1A" # パケット名
    return dev_packet
def positioninfo():
    dev_position = "senser01" # 用途
    return dev_position

class Management():
    # センサデバイスの行う動作を纏めたクラス.
    # Manegmentクラスを定義して経路データの送受信と書き込み(，確認)を行う各モジュールを呼び出す関数を定義する．
    
    def _RoutedataSend(self): # 経路データの送信
        routedata_peripherals1.periph()
        
    def _RoutedataGet(self): # 経路表作成用のデータ取得
        routedata = routeget_centrals1.Centr()
        return routedata
        
    def _RoutedataWrite(self,route): # 経路表作成用データの保存
        with open('data/makeroute_data.txt','w',encoding='utf-8')as f:
            print(route)
            print(type(route))
            f.write(str(route))
        f.close()

    def _chack(self):
        with open('data/makeroute_data.txt',"r",encoding='utf-8')as f:
            print(f.read())
        f.close()

    def _MakeRouteTable(self): # 経路表作成
        #with open("data/makeroute_data.txt",'r',encoding="utf-8")as f:
        #    f.read()
        #f.close()
        makeroute_s1._routemake()
        
    def getdistance(self): # 距離データの取得
        distance = get_s1.distance()
        print("#####")
        print(distance) #ここで絶対にstrにしておく
        print(type(distance))
        distance = str(distance)
        print(type(distance))
        return distance
        
    def SenserdataSend(self,distance): # 作成した経路表に基づく距離データの送信
        senddistance_peripherals1.periph(distance,10)

if __name__ == "__main__":
    mg = Management()
    #data = mg._RoutedataSend()
    #route = mg._RoutedataGet()
    #mg._RoutedataWrite(data)
    #mg._MakeRouteTable()
    distance = mg.getdistance()
    mg.SenserdataSend(distance)

