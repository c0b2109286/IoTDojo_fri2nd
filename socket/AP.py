import network

wifi = network.WLAN(network.STA_IF)
IP = wifi.ifconfig()[0]
print(IP)

def wiFiAccessPoint(ip,mask,gw,dns):
    ap = network.WLAN(network.AP_IF)
    count = 0
    while count < 100:
        try:
            ap.config()
            break
        except:
            count += 1
            print('.',end="")
    ap.ifconfig((ip,mask,gw,dns))
    print("(ip,netmask,gw,dns)=" + str(ap.ifconfig()))
    ap.active(True)
    return ap
    
AP_CONFIG = wiFiAccessPoint(IP,'255.255.255.0',IP,'8.8.8.8')