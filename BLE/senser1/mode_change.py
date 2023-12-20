import ubinascii

def Change(Cmode):
    
    packet = (None, None)
    
    if Cmode is 0:
        packet_list = list(packet)
        #relay5_forsensback
        packet_list[0] = '666f7273656e736261636b' #forsensback
        packet_tuple = packet_list
    
    elif Cmode is 1:
        packet_list = list(packet)
        #relay2_forsenser1
        #packet_list[0] = '666f72' #for
        packet_list[0] = '73656e73657231' #senser1
        packet_tuple = packet_list
        
    elif Cmode is 2:
        packet_list = list(packet)
        packet_list[0] = '746f646576696365' #todevice
        packet_tuple = packet_list

    elif Cmode is 3:
        packet_list = list(packet)
        packet_list[0] = '63616c6c73656e736572' #callsenser
        packet_tuple = packet_list
    
    return packet_tuple
    
if __name__ == "__main__":
    print(ubinascii.hexlify('forsensback'))
    Cmode = 0
    Change(Cmode)
