import route_manegement
import distance_manegement
import condition_manegement
import ubinascii


def MG():
    
    Pmode_change = 0
    Cmode_change = 0
    fn = 'info/DN05.json'
    
    utime.sleep(6)
    
    condition1 = 0
    condition2 = 0
    
    #3 -> 5 -> 7 -> / mode:P0,C0
    fntxt1 = "data/SsRoutetabledata.txt"
    fntxt2 = 'data/SsMakeroute_data.txt'
    fntxt3 = 'data/SsMakeroute_data.txt'
    fnjson1 = 'data/SsRouteinfo.json'
    mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change, fntxt1, fntxt2, fntxt3, fnjson1, condition1)
    condition1 += 1
    
    Pmode_change = mode_change[0]
    Cmode_change = mode_change[1]
    print(Cmode_change)
    print(Pmode_change)
    #Pmode_change = 2
    #Cmode_change = 2
    
    utime.sleep(10)
    utime.sleep(5)
    
    #condition
    #Pmode_change = mode_change[0]
    #Cmode_change = mode_change[1]
    #print(Cmode_change)
    #print(Pmode_change)
    #mode_change = condition_manegement.MGCondition(fn, Pmode_change, Cmode_change, condition2)
    Pmode_change = 3
    Cmode_change = 3
    
    #routemake / 7 -> 1 / Cmode:3,Pmode:2
    fntxt1 = "data/SvRoutetabledata.txt"
    fntxt2 = 'data/SvMakeroute_data.txt'
    fntxt3 = 'data/SvMakeroute_data.txt'
    fnjson1 = 'data/SvRouteInfo.json'
    condition1 = 1
    mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change, fntxt1, fntxt2, fntxt3, fnjson1, condition1)
    
    #condition　/ Cmod
    Pmode_change = mode_change[0]
    Cmode_change = mode_change[1]
    print(Cmode_change)
    print(Pmode_change)
    #condition2 = 1
    #mode_change = condition_manegement.MGCondition(fn, Pmode_change, Cmode_change, condition2)
    Pmode_change = 6
    Cmode_change = 6
    
    utime.sleep(15)
    
    #distance
    distance_manegement.MGDist(fn, Pmode_change, Cmode_change)
    
    #tuples = (1,2)
    #t1 = tuples[0]
    #print(t1) #1
    
if __name__ == "__main__":
    print(ubinascii.hexlify('call'))
    MG()
