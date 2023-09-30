import socket
import ubinascii
import urequests
import time
import json
import pickle

def get():
    
    route = None
    
    url = "http://192.168.193.229:5000/send_to_esp"
    #urequests.head(url)
    print("test")
    
    sendData = {"sign": "get"}
    print(sendData)
    header = {'Content-Type': 'application/json'}
    
    res = urequests.post(url, data=json.dumps(sendData),headers=header)
    print("サーバからのステータスコード：", res.status_code)
    #print(res)
    resp = res.json()
    
    resp = resp["routedata"]
    recv = bytes(resp, "utf-8")
    recv = pickle.loads(recv)
    print(type(recv))
    
    if b'\x80\x04]\x94.' in recv:
        print("空のlistを受け取りました．")
    else:
        recv = recv.replace(b'\x80\x04\x95\x1d', b'')
        recv = recv.replace(b'\x00\x00\x00\x00\x00\x00\x00]\x94(\x8c',b'')
        recv = recv.replace(b'\t', b'')
        recv = recv.replace(b'\x94\x8c', b'\n')
        recv = recv.replace(b'\x94e.', b'')
        recv = recv.replace(b'\x80\x04\x95)', b'')
        recv = recv.replace(b'\x0b',b'')
        recv = recv.replace(b'\x80\x04\x957', b'')
        print(recv)
        route = str(recv,'utf-8')
        print(route)
        print(type(route))
    
    print('終了です')
    return route

if __name__ == "__main__":
    data = get()
    with open('data/routetabledata.txt','w',encoding='utf-8')as f:
        f.write(data)
        f.close()
