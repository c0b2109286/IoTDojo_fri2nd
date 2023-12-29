import route_manegement
import distance_manegement
import ubinascii
import utime


def MG():
    
    Pmode_change = 0
    Cmode_change = 0
    fn = 'info/DN06.json'
    
    utime.sleep(40)
    
    utime.sleep(10)
    
    mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change)
    print("+++++++")
    print(mode_change)
    Pmode_change = mode_change[0]
    Cmode_change = mode_change[1]
    
    utime.sleep(5)
    
    distance_manegement.MGDist(fn, Pmode_change, Cmode_change)
    
    #tuples = (1,2)
    #t1 = tuples[0]
    #print(t1) #1
    
if __name__ == "__main__":
    print(ubinascii.hexlify('senser'))
    MG()
