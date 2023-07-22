import routedata_peripheral7
import routedata_central7
import senddistance_central7
import senddistance_peripheral7
import makeroute7
import ubinascii

def nameinfo():
    dev_name = 7
    return dev_name
def packetinfo():
    dev_packet = "esp32-2A"
    return dev_packet
def positioninfo():
    dev_position = "relay1"
    return dev_position

class Management():
    
    def _RoutedataGet(self):
        get = routedata_central7.Centr()
        return get
        
    def _RoutedataSend(self,routedata):
        send= routedata_peripheral7.periph(routedata,5)
        print(type(send))
        with open("data/senddata1.txt",'w')as f:
            f.write(send)
        f.close()
        return send
    
    def _check(self):
        with open("data/senddata1.txt",'r')as f:
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
        makeroute7._routemake()
        
    def SenserdataGet(self):
        distance = senddistance_central7.Centr()
        return distance
        
    def SenserdataSend(self,distance):
        senddistance_peripheral7.periph(str(distance),5)

if __name__ == "__main__":
    print(ubinascii.hexlify('com8'))
    mg = Management()
    #routedata = mg._RoutedataGet()
    #mg._RoutedataSend(routedata)
    #mg._check()
    #route_data = mg._RoutedataCatch()
    #mg._MakeRouteTable()
    distance = mg.SenserdataGet()
    mg.SenserdataSend(distance)
