import socket
import time

def set_socket():
    host1 = '192.168.2.102' #relay.pyを実行する端末のIPアドレス
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
        transSocket(str_data)
        #str_data = int(str_data)+1 #受信データの編集
        #transSocket(str(str_data))
        time.sleep(0.5)

def transSocket(data):
    print("##### 受信データを転送 #####")
    socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.2.107" #relay2を実行する端末のIPアドレス
    port = 80
    
    try:
        server = (host, port)
        socket2.connect(server)
        socket2.send(data)
        socket2.close()
    except:
        print("error")

if __name__ == "__main__":
    set_socket()