# coding: utf-8

import socket

host1 = '192.168.2.104' #自身のIPアドレス
port1 = 80

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
while True:

    # クライアントからデータを受信
    recvline = connection.recv(4096).decode()

    if recvline == 'bye':
        break
    
    print('クライアントで入力された文字＝' + str(recvline))
        
# クローズ
connection.close()
socket1.close()
print('サーバー側終了です')