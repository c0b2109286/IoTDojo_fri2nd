import time
import json
import urequests
import routedata_getfromserver1
#import sqlite3


def send(senddata):
    url = 'http://192.168.193.73:5000/data' #wifi環境をflaskと一致させる
    
    #with open('sendroutedata.txt', 'r', encoding = 'utf-8')as f:
    #    data = f.read()
    #    print(data)
    
    #print(senddata)
    #print(type(senddata))

    # 送信データ
    sendData = {"message": senddata}
    print(sendData)
    header = {'Content-Type': 'application/json'}

    # postでサーバにJSON形式データを送信し, 送信成功の可否をresに格納
    res = urequests.post(url, data=json.dumps(sendData),headers=header)
    print("サーバからのステータスコード：", res.status_code)
    res.close()
    return 

if __name__ == '__main__':
    dt = "5_2_1_2_0" #time_out
    #dt = "5_2_1_2"
    send(dt)
    print("end")
    data = routedata_getfromserver1.get() #time_out
    #with open('data/routetabledata.txt','w',encoding='utf-8')as f:
    #    f.write(data)
    #    f.close()
    #conn = sqlite3.connect("test.db")
    #cursor = conn.cursor()
