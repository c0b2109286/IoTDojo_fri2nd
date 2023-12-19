import ubinascii

def Change(Cmode):
    
    packet = (None, None)
    
    if Cmode is 0:
        packet_list = list(packet)
        #senser1_toserver
        packet_list[0] = '73656e73657231' #senser1
        packet_tuple = tuple(packet_list)
        #print(packet_tuple)
        
    elif Cmode is 1:
        packet_list = list(packet)
        #relay1_todevice
        packet_list[0] = '746f72656c617932' #torealy2
        packet_tuple = tuple(packet_list)

    elif Cmode is 2:
        packet_list = list(packet)
        packet_list[0] = '5f72656c617932' #relay2
        packet_tuple = tuple(packet_list)
    
    return packet_tuple
    
if __name__ == "__main__":
    print(ubinascii.hexlify('relay2'))
    Cmode = 0
    packet = Change(Cmode)
    print(packet)
