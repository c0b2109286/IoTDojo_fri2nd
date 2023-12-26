import route_manegement
import distance_manegement
import makeroute
import ubinascii
import time


def MG():
    
    Pmode_change = 0
    Cmode_change = 0
    fn = 'info/DN04.json'
    condition1 = 0
    mode_change = ()
    
    # performe route building
    mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change, condition1)
    print("+++++++")
    print(mode_change)
    Pmode_change = mode_change[0]
    Cmode_change = mode_change[1]
    condition1 += 1
    
    #time.sleep(5)

    # performe route building
    mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change, condition1)
    print("+++++++")
    print(mode_change)
    Pmode_change = mode_change[0]
    Cmode_change = mode_change[1]

    fntxt = 'data/makeroute_data.txt'
    fnjson = 'data/routeinfo.json'
    makeroute._routemake(fntxt, fnjson)
    
    time.sleep(10)

    # send the senser data to server
    for i in range(3):
        distance_manegement.MGDist(fn, Pmode_change, Cmode_change)
        utime.sleep(1)
    
    #tuples = (1,2)
    #t1 = tuples[0]
    #print(t1) #1
    
if __name__ == "__main__":
    print(ubinascii.hexlify('forsenser'))
    MG()
