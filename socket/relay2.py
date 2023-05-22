import socket
import time

sf_name = "server" #サーバのファイル名
cf_name = "client" #クライアントのファイル名
rf_name = "relay" #中継のファイル名

def set_socket():
    host1 = '192.168.2.107' #自身のIPアドレス
    #host1 = wifi.ifconfig()[0]
    #host1 = '0.0.0.0'
    port1 = 80

    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.bind((host1, port1))
    socket1.listen(1)

    print('クライアントからの入力待ち状態')
    # コネクションとアドレスを取得
    connection, address = socket1.accept()
    print('接続したクライアント情報:'  + str(address))
    recvline = ''
    while True:
        if recvline == 'bye':
            break        
        data = connection.recv(1024)
        str_data = data.decode()      
        print("受信データ:", str_data)
        #connection.close()
        str_data = int(str_data)+1
        transSocket(str(str_data))
        #transSocket(str_data)
        time.sleep(0.5)

def transSocket(data):
    print("##### 受信データを転送 #####")
    socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.2.104" #PCのIPv4アドレス
    #host = "192.168.2.107" #R2のIPアドレス
    port = 80
    
    try:
        server = (host, port)
        socket3.connect(server)
        socket3.send(data)
        socket3.close()
    except:
        print("error")


if __name__ == "__main__":
    set_socket()