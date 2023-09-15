import socket
#import pickle
import ubinascii

def get():
    host1 = '192.168.229.159' #自身のIPアドレス
    port1 = 80
    
    GET = True

    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.bind((host1, port1))
    socket1.listen(1)

    print('クライアントからの入力待ち状態')

    # コネクションとアドレスを取得
    connection, address = socket1.accept()
    print('接続したクライアント情報:'  + str(address))

    # 無限ループ　byeの入力でループを抜ける
    recvline = ''
    sendline = ''
    num = 0
    #while GET is True:

        # クライアントからデータを受信
    recvline = connection.recv(4096)
        #if recvline == 'bye':
        #    break
    
    #getdata = pickle.loads(recvline)
    print(type(recvline))
    print(recvline)
    if ')' in recvline:
        gd = recvline.replace(b'\x80\x04\x95)\x00\x00\x00\x00\x00\x00\x00]\x94(]\x94\x8c\x07', b'')
        gd = gd.replace(b'\x94a]\x94\x8c\r', b'')
        gd = gd.replace(b'\x94ah\x01h\x03e.', b'')
        #gd = gd.replace(b'_',b'')

    if ',' in recvline:
        gd = recvline.replace(b'\x80\x04\x95\x19\x00\x00\x00\x00\x00\x00\x00\x8c\x15',b'')
        gd = gd.replace(b'\x94.',b'')
        #gd = gd.replace(b'_',b'')
        gd = gd.replace(b',',b'\n')
    #getdata = int(ubinascii.unhexlify(gd), 'utf-8')

    print(gd)
    getdata = gd.decode('utf-8')

    print('経路データ' + getdata)
    print(type(getdata))
        
            
    # クローズ
    connection.close()
    socket1.close()
    print('サーバー側終了です')
    return getdata

if __name__ == "__main__":
    get()
