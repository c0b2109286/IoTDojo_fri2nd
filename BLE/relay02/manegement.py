
import route_manegement
import distance_manegement
import makeroute
import ubinascii
import utime


def MG():
    
    Pmode_change = 0
    Cmode_change = 0
    fn = 'info/DN02.json'
    
    # Perfoem route building
    utime.sleep(3)
    mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change)
    print("+++++++")
    print(mode_change)
    
    utime.sleep(5)

    fntxt = 'data/makeroute_data.txt'
    fnjson = 'data/routeinfo.json'
    makeroute._routemake(fntxt, fnjson)
    
    # wait for other route building
    utime.sleep(40)
    Pmode_change = 2
    Cmode_change = 2
    print(Pmode_change)
    print(Cmode_change)
    
    utime.sleep(10)
    utime.sleep(15)
    print("distance")

    # send the senser data to server
    for i in range(2):
        distance_manegement.MGDist(fn, Pmode_change, Cmode_change)
        utime.sleep(15)

if __name__ == "__main__":
    print(ubinascii.hexlify('forsenser'))
    MG()
