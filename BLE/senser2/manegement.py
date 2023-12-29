import route_manegement
import distance_manegement
import condition_manegement
import ubinascii
    
def MG():
    
    mode_change = ()
    Pmode_change = 0
    Cmode_change = 0
    fn = 'info/SN02.json'
    condition1 = 0
    utime.sleep(12)
    
    #中継器機能
    mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change, condition1)
    print("+++++++")
    print(mode_change) # P:1,C:1
    
    #経路構築開始の通知を受け取る（Central）
    #Pmode_change = mode_change[0] #P:1
    #Cmode_change = mode_change[1] #P:1
    #condition = 0
    #mode_change = condition_manegement.MGCondition(fn, Pmode_change, Cmode_change, condition)
    #print("+++++++")
    #print(mode_change)
    #condition += 1
    Pmode_change = 1
    Cmode_change = 2
    condition1 = 1
    
    utime.sleep(15)
    utime.sleep(5)
    
    #センサー機能
    Pmode_change = mode_change[0] #P:1
    Cmode_change = mode_change[1] #C:2
    mode_change = route_manegement.MGRoute(fn, Pmode_change, Cmode_change, condition1)
    print("+++++++")
    print(mode_change)
    
    utime.sleep(9)
    
    #距離取得開始の通知送信(Peripheral)
    #Pmode_change = mode_change[0] #P:2
    #Cmode_change = mode_change[1] #C:3
    #mode_change = condition_manegement.MGCondition(fn, Pmode_change, Cmode_change, condition)
    #print("+++++++")
    #print(mode_change)
    
    utime.sleep(5)
    Pmode_change = 3
    Cmode_change = 3
    
    #距離計測
    #Pmode_change = mode_change[0] #P:3
    #Cmode_change = mode_change[1] #C:3
    
    utime.sleep(5)
    
    
    distance_manegement.MGDist(fn, Pmode_change, Cmode_change)
    
    #tuples = (1,2)
    #t1 = tuples[0]
    #print(t1) #1
    
if __name__ == "__main__":
    print(ubinascii.hexlify('relay1'))
    MG()
