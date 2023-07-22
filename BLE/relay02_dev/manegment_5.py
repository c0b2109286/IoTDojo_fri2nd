import routesendtoserver5
import routedata_central5
import senddistance_central5
import distancesendtoserver5
#import senddistance_peripheral
#import makeroute
import ubinascii

def nameinfo():
    dev_name = 5
    return dev_name
def packetinfo():
    dev_packet = "esp32-3A"
    return dev_packet
def positioninfo():
    dev_position = "relay12"
    return dev_position

class Management():
    
    def _RoutedataGet(self):
        get = routedata_central5.Centr()
        return get
        
    def _RoutedataSendtoServer(self,senddata):
        routesendtoserver5.send(senddata)
    
    def _check(self):
        with open("data/senddata2.txt",'r')as f:
            print(f.readline())
        f.close()

    def _RoutedataCatch(self):
        data = central.Centr()
        print(data)
        return data

    def _MakeRouteTable(self,data):
        with open("routedata_test.txt",'w',encoding="utf-8")as f:
            f.write(data)
        f.close()
        makeroute._routemake()
        
    def SenserdataGet(self):
        distance = senddistance_central5.Centr()
        return distance
        
    def SenserdataSend(self,distance):
        distancesendtoserver5.send(distance)

if __name__ == "__main__":
    print(ubinascii.hexlify('com5'))
    mg = Management()
    #routedata = mg._RoutedataGet()
    #senddata = routedata + '_' + str(nameinfo())
    
    #mg._RoutedataSendtoServer(senddata)
    #mg._check()
    
    #route_data = mg._RoutedataCatch()
    #mg._MakeRouteTable()
    distance = mg.SenserdataGet()
    
    #dist = distance.replace(" ",'')
    dist = distance.replace('\x00','')
    print(dist)
    print(type(dist))
    
    mg.SenserdataSend(dist)
