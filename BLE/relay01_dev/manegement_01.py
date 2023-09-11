import routedata_peripheral01
import routedata_central01
import senddistance_central01
import senddistance_peripheral01
import makeroute_01
import ubinascii
from machine import Timer
import micropython,time


# def nameinfo():
#     dev_name = 1
#     return dev_name
# def packetinfo():
#     dev_packet = "esp32-2A"
#     return dev_packet
# def positioninfo():
#     dev_position = "relay1"
#     return dev_position

class Management():
    def _RoutedataGet(self):
        global stop
        stop = True
        get = routedata_central01.Centr()
        return get
        
    def _RoutedataSend(self,routedata):
        send= routedata_peripheral01.periph(routedata,5)
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
        makeroute_01._routemake()
        
    def SenserdataGet(self):
        distance = senddistance_central01.Centr()
        return distance
        
    def SenserdataSend(self,distance):
        senddistance_peripheral01.periph(str(distance))

if __name__ == "__main__":
    connection = 0
    stop = False
    SEND = True
    mg = Management()
    
    while SEND is True and connection < 3:
        if stop == True:
            break
        routedata = mg._RoutedataGet()
        mg._RoutedataSend(routedata)
        connection += 1
    timer = Timer(0)
    routedata = timer.init(mode=Timer.ONE_SHOT, period=3000, callback = mg._RoutedataCatch())
    
    # route_data = mg._RoutedataCatch()
    
    mg._MakeRouteTable()
    distance = mg.SenserdataGet()
    mg.SenserdataSend(distance)

