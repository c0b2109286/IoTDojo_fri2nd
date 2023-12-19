import time
import json
import urequests

#def send():
def send(senddata):
    url = 'http://[IP]:5000/data' #wifi環境をflaskと一致させる
    
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
    #urequests.post(url, data=json.dumps(sendData),headers=header)
    res.close()
    print("サーバからのステータスコード：", res.status_code)


if __name__ == '__main__':
    senddata = "test"
    send(senddata)
