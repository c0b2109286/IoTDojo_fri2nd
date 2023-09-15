import routedata_sendtoserver2
import routedata_central2
import senddistance_central2
import distance_sendtoserver2
#import senddistance_peripheral
#import makeroute
import ubinascii
import json
import routedata_getfromserver1
import routesendtodevice_peripheral1

class Management():
    
    def _RoutedataGet(self):
        get = routedata_central2.Centr()
        return get
        
    def _RoutedataSendtoServer(self,senddata):
        routedata_sendtoserver2.send(senddata)
    
    #実際に受け取るときには必要
    def _RouteGetFromServer(self):
        GS = routedata_getfromserver1.get()
        return GS
        
    def _RoutedataWrite(self, data):
        with open('data/routeinfo.txt','w', encoding="utf-8")as f:
            print(data)
            #print(type(data))
            f.write(data)
            f.close
            
    def _SendRouteForDevice(self,data):
        routesendtodevice_peripheral1.periph(data)
        

    def _MakeRouteTable(self,data):
        #with open("routedata_test.txt",'w',encoding="utf-8")as f:
        #    f.writelines(data)
        #f.close()
        makeroute._routemake()
        
    def SenserdataGet(self):
        distance = senddistance_central2.Centr()
        return distance
        
    def SenserdataSend(self,distance):
        distance_sendtoserver2.send(distance)

if __name__ == "__main__":
    print(ubinascii.hexlify('esp32'))
    mg = Management()
    
    routedata = mg._RoutedataGet()
    
    jf_open = open('info/DN02.json', 'r')
    jf_load = json.load(jf_open)
    gapname = jf_load["device_number"]

    route = routedata + '_' + str(gapname)
    print(route)
    print(len(route))
    if len(route) is 3:
        hop = len(route) - 2
    if len(route) is 5:
        hop = len(route) - 3
    if len(route) is 7:
        hop = len(route) -4
    if len(route) is 9:
        hop = len(route) -5

    senddata = route + '_' + str(hop)
    print(senddata)
    
    response = mg._RoutedataSendtoServer(senddata)
    
    getroutedata = mg._RouteGetFromServer()
    
    #getroutedata = getroutedata.replace(',','\n')
    
    mg._RoutedataWrite(getroutedata)
    
    mg._SendRouteForDevice(getroutedata)
    
    #route_data = mg._RoutedataCatch()
    #mg._MakeRouteTable()
    
    distance = mg.SenserdataGet()
    
    #dist = distance.replace(" ",'')
    #dist = distance.replace('\x00','')
    #print(dist)
    #print(type(dist))
    
    mg.SenserdataSend(distance)
