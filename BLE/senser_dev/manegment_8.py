import routedata_peripheral8
import routeget_central8
import senddistance_peripheral8
#import makeroute
import get

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
        routedata_peripheral8.periph()
        
    def _RoutedataGet(self):
        routedata = routeget_central8.Centr()
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
        makeroute._routemake()
        
    def getdistance(self):
        distance = get.distance()
        return distance
        
    def SenserdataSend(self,distance):
        senddistance_peripheral.periph(str(distance))

if __name__ == "__main__":
    mg = Management()
    data = mg._RoutedataSend()
    route = mg._RoutedataGet()
    #mg._RoutedataWrite(data)
    #mg._MakeRouteTable()
    #distance = mg.getdistance()
    #mg.SenserdataSend(distance)
