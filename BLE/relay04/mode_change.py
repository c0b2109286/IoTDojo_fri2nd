import ubinascii
def Change(Cmode):
    
    packet = (None, None)
    
    if Cmode is 0:
        packet_list = list(packet)
        packet_list[0] = '73656e73657231' #senser1
        packet_tuple = tuple(packet_list)
        #print(packet_tuple)
        
    elif Cmode is 1:
        packet_list = list(packet)
        #packet_list[0] = '746f72656c7934' 
        packet_list[0] = '746f72656c617934' #torelay4
        packet_tuple = tuple(packet_list)

    elif Cmode is 2:
        packet_list = list(packet)
        packet_list[0] = '746f736572766572' #toserver
        packet_tuple = tuple(packet_list)
        
    elif Cmode is 3:
        packet_list = list(packet)
        packet_list[0] = '746f72656c617934' #torelay4
        packet_tuple = tuple(packet_list)
        
    elif Cmode is 4:
        packet_list = list(packet)
        packet_list[0] = '72656c617934' #relay4
        packet_tuple = tuple(packet_list) 
    
    return packet_tuple
    
if __name__ == "__main__":
    print(ubinascii.hexlify('toserver'))
    Cmode = 0
    packet = Change(Cmode)
    print(packet)
