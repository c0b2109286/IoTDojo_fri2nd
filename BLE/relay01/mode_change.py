import ubinascii

def Change(Cmode):
    
    packet = (None, None)
    
    if Cmode is 0:
        packet_list = list(packet)
        #relay2_toserver
        #relay4_toserver
        packet_list[0] = '72656c617932' #relay2
        packet_tuple = tuple(packet_list)
        #print(packet_tuple)
        
    if Cmode is 1:
        packet_list = list(packet)
        #relay2_toserver
        #relay4_toserver
        packet_list[0] = '72656c617934' #relay4
        packet_tuple = tuple(packet_list)
        #print(packet_tuple)
        
    if Cmode is 2:
        packet_list = list(packet)
        #relay4_toserver
        packet_list[0] = '72656c617934' #relay4
        packet_tuple = tuple(packet_list)
        #print(packet_tuple)
    
    if Cmode is 3:
        packet_list = list(packet)
        #relay4_toserver
        packet_list[0] = '72656c617934' #relay4
        packet_tuple = tuple(packet_list)
        #print(packet_tuple)
        
    #elif Cmode is 1:
    #    packet_list = list(packet)
    #    #relay4_toserver
    #    packet_list[0] = '72656c617934' #relay4
    #    packet_tuple = tuple(packet_list)

    elif Cmode is 4:
        packet_list = list(packet)
        packet_list[0] = '72656c617934' #relay4
        packet_list[1] = '72656c617932' #relay2
        packet_tuple = tuple(packet_list)
        
    elif Cmode is 5:
        packet_list = list(packet)
        packet_list[0] = '72656c617931' #relay1
        packet_tuple = tuple(packet_list)
        
    elif Cmode is 6:
        packet_list = list(packet)
        packet_list[0] = '72656c617934' #relay4
        packet_list[1] = '72656c617932' #relay2
        packet_tuple = tuple(packet_list)
    
    
    return packet_tuple
    
if __name__ == "__main__":
    print(ubinascii.hexlify('relay5'))
    Cmode = 0
    packet = Change(Cmode)
    print(packet)
