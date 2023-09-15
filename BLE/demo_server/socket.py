import socket
import pickle
import json
def data():
    data = '5_2_1'
    data1 = data + '_' + '1'    
    data2 = '2_6_7_3_1_4' + '_' + '2'
    line = data1 + ',' + data2
    #data1 = [data + '_' + '1']    
    #data2 = ['5_6_7_3_1_4' + '_' + '2']
    #line = []
    #for i in range(2):
    #    line.append(data1)
    #    line.append(data2)
    return line

def send(line):
    ip = socket.gethostbyname(socket.gethostname())
    print(ip)

    ip1 = '192.168.229.159'
    port1 = 80
    server = (ip1, port1)

    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect(server)


    # サーバに送信
    senddata = pickle.dumps(line)
    print(type(senddata))
    socket1.send(senddata)
    print(senddata)

    #socket1.send(line)

    socket1.close()
    print('クライアント側終了です')

if __name__ == "__main__":
    dt = data()
    send(dt)
