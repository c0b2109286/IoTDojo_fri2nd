import ubinascii
def Change(Cmode):
    
    packet = (None, None)
    
    if Cmode is 0:
        packet_list = list(packet)
        #senser1_toserver
        packet_list[0] = '73656e73657231' #senser1
        packet_tuple = tuple(packet_list)
        
    elif Cmode is 1:
        packet_list = list(packet)
        #senser2_todevback
        packet_list[0] = '746f6465766261636b' #todevback
        packet_tuple = tuple(packet_list)

    elif Cmode is 2:
        #esp32_senser1
        packet_list = list(packet)
        packet_list[0] = '73656e73657231' #senser1
        packet_tuple = tuple(packet_list)
        
        
    elif Cmode is 3:
        packet_list = list(packet)
        packet_list[0] = '73656e73657232' #senser2
        packet_tuple = tuple(packet_list)
        
    elif Cmode is 4:
        packet_list = list(packet)
        packet_list[0] = '746f72656c617935' #torelay5
        packet_tuple = tuple(packet_list)
    
    elif Cmode is 6:
        packet_list = list(packet)
        packet_list[0] = '72656c617935' #relay5
        packet_tuple = tuple(packet_list)
    
    return packet_tuple
    
if __name__ == "__main__":
    print(ubinascii.hexlify('torelay5'))
    Cmode = 1
    packet = Change(Cmode)
    print(packet)
