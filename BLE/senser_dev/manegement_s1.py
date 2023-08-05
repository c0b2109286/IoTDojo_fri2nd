import routedata_peripherals1
import routeget_centrals1
import senddistance_peripherals1
import makeroute_s1
import get_s1

def nameinfo():
    dev_name = 8
    return dev_name
def packetinfo():
    dev_packet = "esp32-1A"
    return dev_packet
def positioninfo():
    dev_position = "senser01"
    return dev_position

class Management():
        
    def _RoutedataSend(self):
        routedata_peripherals1.periph()
        
    def _RoutedataGet(self):
        routedata = routeget_centrals1.Centr()
        return routedata
        
    def _RoutedataWrite(self,route):
        with open('data/makeroute_data.txt','w',encoding='utf-8')as f:
            print(route)
            print(type(route))
            f.write(str(route))
        f.close()

    def _chack(self):
        with open('data/makeroute_data.txt',"r",encoding='utf-8')as f:
            print(f.read())
        f.close()

    def _MakeRouteTable(self):
        #with open("data/makeroute_data.txt",'r',encoding="utf-8")as f:
        #    f.read()
        #f.close()
        makeroute_s1._routemake()
        
    def getdistance(self):
        distance = get_s1.distance()
        print("#####")
        print(distance) #ここで絶対にstrにしておく
        print(type(distance))
        distance = str(distance)
        print(type(distance))
        return distance
        
    def SenserdataSend(self,distance):
        senddistance_peripherals1.periph(distance,10)

if __name__ == "__main__":
    mg = Management()
    #data = mg._RoutedataSend()
    #route = mg._RoutedataGet()
    #mg._RoutedataWrite(data)
    #mg._MakeRouteTable()
    distance = mg.getdistance()
    mg.SenserdataSend(distance)

