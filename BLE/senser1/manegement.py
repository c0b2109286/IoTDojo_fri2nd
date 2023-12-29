import route_manegement
import distance_manegement
import condition_manegement
import ubinascii
    
def MG():
    
    mode_change = ()
    Pmode_change = 0
    Cmode_change = 0
    fn = 'info/SN01.json'
    condition1 = 0
    condition2 = 0
    
    #センサー役割
    mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change,condition2)
    condition2 += 1
    print("+++++++")
    print(mode_change)
    
    Pmode_change = mode_change[0] #Pmode 1
    Cmode_change = mode_change[1] #Cmode 2
    
    #経路構築開始伝える
    #mode_change = condition_manegement.MGCondition(fn, Pmode_change, Cmode_change, condition1)
    Pmode_change += 1
    print("+++++++")
    Cmode_change = 2
    mode_change = (Pmode_change, Cmode_change)
    print(mode_change)
    condition1 += 1
    
    Pmode_change = mode_change[0] #mode 2
    Cmode_change = mode_change[1] #mode 2
    #Pmode_change = 2
    #Cmode_change = 2
    
    utime.sleep(5)
    
    #中継器役割
    #mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change, condition2)
    utime.sleep(30)
    #print("+++++++")
    #print(mode_change)
    
    #Pmode_change = mode_change[0] #mode 3
    #Cmode_change = mode_change[1] #mode 3
    Pmode_change = 3
    Cmode_change = 3
    
    #距離開始受け取り
    #mode_change = condition_manegement.MGCondition(fn, Pmode_change, Cmode_change, condition1)
    Cmode_change += 1
    print("+++++++")
    Pmode_change = 3
    mode_change = (Pmode_change, Cmode_change)
    print(mode_change)
    condition1 += 1
    
    Pmode_change = mode_change[0] #mode 3
    Cmode_change = mode_change[1] #mode 4
    #Pmode_change = 3
    #Cmode_change = 4
    
    #utime.sleep(5)
    utime.sleep(3)
    
    #距離
    for i in range(2):
        distance_manegement.MGDist(fn, Pmode_change, Cmode_change)
        utime.sleep(5)
    
    #tuples = (1,2)
    #t1 = tuples[0]
    #print(t1) #1
    
if __name__ == "__main__":
    print(ubinascii.hexlify('back'))
    MG()
