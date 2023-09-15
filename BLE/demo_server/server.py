from flask import Flask, request, jsonify, render_template
import json
import socket

res = None

# Flaskアプリケーションの作成
app = Flask(__name__)

# GETリクエストに応答するエンドポイントの作成
@app.route('/data', methods=['GET','POST'])
def receive():
    global res

    if request.method == 'POST':
        data= request.get_json()
        res = str(data["message"])
        print(res)
        print(type(res))
        #result = send_to_esp(res)
    #return jsonify({'result' : res})
    return render_template('view.html',result = res)

# @app.route('/send_to_esp', methods=['GET','POST'])
# def send_to_esp(data):
#     # ESP32_IP = "192.168.229.159"  # 例: '192.168.1.100'
#     # PORT = 80
#     # # TCP接続
#     # MESSAGE = [[data + '_' + '1'],['5_6_7_3_1_4' + '_' + '2']]
#     # print(MESSAGE)
#     # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # client_socket.connect((ESP32_IP, PORT))
#     # client_socket.send(MESSAGE.encode())
#     # client_socket.close()
#     # #return render_template('view.html',result = res)
#     # return 

#     ip1 = '192.168.229.159'
#     port1 = 80
#     server = (ip1, port1)

#     socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     socket1.connect(server)

#     line = ''
#     data = '5_2_1'
#     while line != 'bye':
#         # 標準入力からデータを取得
#         print('値を入力して下さい')
#         line = [[data + '_' + '1'],['5_6_7_3_1_4' + '_' + '2']]
        
#         # サーバに送信
#         socket1.send(line.encode("UTF-8"))

#     socket1.close()
#     print('クライアント側終了です')

# サーバを起動
if __name__ == '__main__':
    # data = app.run(debug=True, host='0.0.0.0', port=80)
    # print("******")
    # print(data)
    app.run(debug=True, host='0.0.0.0', port=80)
