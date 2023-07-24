from flask import Flask, request, jsonify, render_template
import json

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
    return render_template('view.html',result = res)

# サーバを起動
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
