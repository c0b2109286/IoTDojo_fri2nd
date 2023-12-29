import ubinascii
def Change(Cmode):
    
    packet = (None, None)
    
    if Cmode is 0:
        #senser2_toserver
        packet_list = list(packet)
        packet_list[0] = '73656e73657232' #senser2
        packet_tuple = packet_list
        #print(packet_tuple)
        
    elif Cmode is 1:
        packet_list = list(packet)
        packet_list[0] = '746f72656c617936' #torelay6
        packet_tuple = packet_list

    elif Cmode is 2:
        #esp32_senser2
        packet_list = list(packet)
        packet_list[0] = '72656c617936' #relay6
        packet_tuple = packet_list
    
    return packet_tuple
    
if __name__ == "__main__":
    print(ubinascii.hexlify('torelay6'))
    Cmode = 1
    packet = Change(Cmode)
    print(packet)
