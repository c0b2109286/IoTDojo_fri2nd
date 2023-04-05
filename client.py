import socket

ip1 = '192.168.2.102' #relayを実行する端末のIP
port1 = 80
server = (ip1, port1)

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket1.connect(server)

line = ''
while line != 'bye':
    # 標準入力からデータを取得
    print('値を入力して下さい')
    line = input('>>>')
    
    # サーバに送信
    socket1.send(line.encode("UTF-8"))

socket1.close()
print('クライアント側終了です')