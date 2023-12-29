import ubinascii

def Change(Cmode):
    
    packet = (None, None)
    
    if Cmode is 0:
        #relay5_forsens
        packet_list = list(packet)
        packet_list[0] = '72656c617935' #relay5
        packet_tuple = packet_list
     
    elif Cmode is 1:
        #esp32_relay5
        packet_list = list(packet)
        packet_list[0] = '72656c617935' #relay5
        packet_tuple = packet_list
    
    elif Cmode is 2:
        #relay6_forsenser2
        packet_list = list(packet)
        packet_list[0] = '746f73656e73657232' #tosenser2
        packet_tuple = packet_list
        print(packet_tuple)
        
    return packet_tuple
    
if __name__ == "__main__":
    print(ubinascii.hexlify('tosenser2'))
    Cmode = 0
    Change(Cmode)
