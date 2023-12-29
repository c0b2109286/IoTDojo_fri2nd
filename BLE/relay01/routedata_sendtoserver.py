import time
import json
import urequests
import routedata_getfromserver
#import sqlite3


def send(senddata, url):
    url = url + '/data' #wifi環境をflaskと一致させる
    
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
    #dt = "5_0_0_0" #time_out
    dt = "3_2_1_2"
    url = 'http://192.168.14.73:5000'
    send(dt, url)
    print("end")
