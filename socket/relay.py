import socket
import network
import time
import _thread

ap = None
ls = None
IP = None

def wiFiAccessPoint(ip,mask,gw,dns):
    global IP
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
def set_socket():
    global ls
    while True:
        print('クライアントからの入力待ち状態')
        connection, address = ls.accept()
        print('接続したクライアント情報:'  + str(address))
        recvline = ''

        if recvline == 'bye':
            break        
        data = connection.recv(1024)
        str_data = data.decode()      
        print("受信データ:", str_data)
        #connection.close()
        transSocket(str_data)
        #str_data = int(str_data)+1 #受信データの編集
        #transSocket(str(str_data))
        time.sleep(0.5)

def transSocket(data):
    print("##### 受信データを転送 #####")
    socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.2.104" #relay2を実行する端末のIPアドレス
    port = 80
    
    try:
        server = (host, port)
        socket2.connect(server)
        socket2.send(data)
        socket2.close()
    except:
        print("error")

def main():
    global ls
    global IP
    wifi = network.WLAN(network.STA_IF)
    IP = wifi.ifconfig()[0]
    print(IP)
    wiFiAccessPoint(IP,'255.255.255.0',IP,'8.8.8.8')
    #wifi= network.WLAN(network.STA_IF)
    ip = wifi.ifconfig()[0]
    #print(ip)
    ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #ls = socket.socket()
    ls.bind(('', 80))
    ls.listen(5)
    #ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _thread.start_new_thread(set_socket,())

if __name__ == "__main__":
    main()