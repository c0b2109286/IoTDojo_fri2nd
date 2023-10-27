import folium
from flask import Flask,render_template,request,redirect,url_for
from flask_socketio import SocketIO, emit
from folium.features import CustomIcon
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from datetime import datetime
import itertools
import socket
import re
import sqlite3
import pickle
TOILETA=0
GARBAGE=0
TOILETB=0
reseta=0
resetb=0
route_id = 0
res = None
send_list = []
table = []



app = Flask(__name__)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location.db'
db = SQLAlchemy(app) 


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gps = db.Column(db.Integer, nullable=True)
    num_gps = db.Column(db.Integer)
    ins = db.Column(db.String(100))
    esp_name = db.Column(db.String(100))

class route(db.Model):
    id = db.Column(db.String, primary_key=True)
    route = db.Column(db.String, nullable=True)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.String(100))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))
    
"""ここからログイン"""

# データベースモデルの定義
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# ログインページの表示
@app.route('/login')
def login():
    return render_template('login.html')

# ログインの処理
@app.route('/login_post', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    # ユーザーの認証
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        # ログイン成功時の処理（例：メインページにリダイレクト）
        return redirect(url_for('main'))
    else:
        # ログイン失敗時の処理（例：エラーメッセージの表示）
        error = 'Invalid username or password'
        return render_template('login.html', error=error)

# メインページの表示
@app.route('/main')
def main():
    return 'Welcome to the main page!'
    


"""ここから管理者"""
# 経路表を作成する関数
def mk_routing_table():
    sensor_set = set()
    posts = route.query.all()
    for post in posts:
        sensor_set.add(int(post.route.split("_")[0]))
    
    routing_table = []
    for i in sensor_set:
        plus_tabele = []
        for post in posts:
            if int(post.route.split("_")[0]) == i:
                if plus_tabele:
                    if int(plus_tabele[0].split("_")[-1]) > int(post.route.split("_")[-1]):
                        plus_tabele.insert(0, post.route)

                    elif int(plus_tabele[0].split("_")[-1]) == int(post.route.split("_")[-1]):
                        if int(plus_tabele[-1].split("_")[-1]) == int(post.route.split("_")[-1]):
                            plus_tabele.append(post.route)
                        else:
                            num = 0
                            for plus_route in plus_tabele:
                                if int(plus_route.split("_")[-1]) > int(post.route.split("_")[-1]):
                                    plus_tabele.insert(num, post.route)
                                    break
                                else:
                                    num += 1
                    else:
                        plus_tabele.append(post.route)
                else:
                    plus_tabele.append(post.route)
        routing_table.append(plus_tabele)
    print(routing_table)
    return routing_table

# 経路表からデータ送信に使用する経路をリストにする関数
def mk_routes_num():
    routes_num = []
    routing_table = mk_routing_table()
    for routes in routing_table:
        num_list = []
        for num in routes[0].split("_")[:-1]:
            num_list.append(int(num))
        routes_num.append(num_list)
    return routes_num

# 黒丸を描く全てのノードをリストにする関数
def mk_all_node():
    posts = route.query.all()
    num_set = set()
    for post in posts:
        for num in post.route.split("_")[1:-1]:
            num_set.add(int(num))
    return list(num_set)

# ノード動詞のつながりをタプルにしてリストに入れる関数
def mk_all_route():
    posts = route.query.all()
    line_set = set()
    for post in posts:
        for i in range(len(post.route.split("_"))-2):
            line_set.add((int(post.route.split("_")[i]),int(post.route.split("_")[i+1])))
    return list(line_set)

#numのgpsを返答
def get_gps(num):
    posts = Post.query.all()
    for post in posts: 
        if int(post.id) == int(num):
            return post.gps.split(",")

#numのgpsナンバーを返答
def get_num_gps(num):
    posts = Post.query.all()
    for post in posts:
        if int(post.id) == int(num):
            return post.num_gps.split(",")

#numのespを返答
def get_ins(num):
    posts = Post.query.all()
    for post in posts: 
        if int(post.id) == int(num):
            return post.ins

#numのespの名前を返答
def get_ins_name(num):
    posts = Post.query.all()
    for post in posts: 
        if int(post.id) == int(num):
            return post.esp_name

# numのセンサからのルートを返す関数
def mk_route(num):
    routes_num = mk_routes_num()
    for line in routes_num:
        if line[0] == num:
            route = []
            for i in range(len(line)-1):
                route.append((line[i],line[i+1]))
    return route

# 使っているルートのテキストを返す関数
def mk_route_txt(loc):
    route = {}
    routes_num = mk_routes_num()
    for route_num in routes_num:
        route_txt = f"{get_ins_name(route_num[0])} : "
        for num in route_num:
            route_txt += str(num)
            if num != 1:
                route_txt += " → "
        route[get_ins_name(route_num[0])] = route_txt
    print(route)

    if loc == "ALL": return route.values()
    else: return [route[loc]]

# 経路が重なった
def judge_overlap():
    route_list = []
    routes_num = mk_routes_num()
    for route in routes_num:
        route_list.append(mk_route(route[0]))

    judge_num_list = []
    for pair in itertools.combinations(route_list, 2):
        if set(pair[0])&set(pair[1]):
            judge_num_list.append(pair[0][0][0])    
    return judge_num_list


def fetch_all_ids():
    # データベースへの接続（データベースが存在しない場合は新規作成）
    conn = sqlite3.connect("./instance/location.db")
    # カーソルオブジェクトの作成
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM breakesp')
    res=[row[0] for row in cursor.fetchall()]
    conn.close()
    return res

def fetch_gps_values(i):
    # データベースへの接続（データベースが存在しない場合は新規作成）
    conn = sqlite3.connect("./instance/location.db")
    # カーソルオブジェクトの作成
    cursor = conn.cursor()
    # IDリストに基づいてGPSの値を取得
    cursor.execute('SELECT gps FROM post WHERE id=?', (i,))
    result = cursor.fetchone()
    if result:
        gps_values =result[0].split(',')
        conn.close()
    return gps_values

# 壊れたESPを含む経路をデータベースから削除する
def delete_route():
    posts = route.query.all()
    break_esp=fetch_all_ids()
    break_esp = [int(i) for i in break_esp]
    for post in posts:
        for num in post.route.split("_")[:-1]:
            if int(num) in break_esp:
                print(post)
                db.session.delete(post)
                db.session.commit()
#-------------------------------------------------------------

@app.route('/admin', methods = ["GET", "POST"])
def admin():
    if request.method == 'GET':
        location = "ALL"
        print("GET")
        route = mk_route_txt(location)
        return render_template('index2.html', location = location, route = route)
    
    else:
        location = request.form.get("btn", None)
        print(location)
        if location == "ログアウト":
            return render_template("index.html")
        try:
            route = mk_route_txt(location)
            return render_template('index2.html', location = location, route = route)
        except:
            pass
        return render_template('index2.html', location = [], route = [])


@app.route('/map/<location>',methods = ["GET"])
def foliummap(location):
    ## マップ全体の決めごと

    start_cords=(35.67061628919986, 139.69567437962016)             #マップの中心位置
    folium_map = folium.Map(location=start_cords, zoom_start=17)    #マップの倍率
    route, color = mk_all_route(),"gray"                            #ルートに関する代入
    break_esp=fetch_all_ids()#壊れたespの特定
    
    delete_route()
    
    # 灰色の線を描く
    for loc in route:
        folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = "gray").add_to(folium_map)

    # 各ノードの番号スタンプを描く
    for i in range(1,7):
        a = f"./image/num{i}.png"
        icon = CustomIcon(icon_image = a, icon_size = (80, 75), icon_anchor = (35, 35), popup_anchor = (0, 0))
        folium.Marker(location=get_num_gps(i),icon = icon).add_to(folium_map)


    ## 押されたボタンがALLの場合
    if location == "ALL":
        # 重なっている経路がないか検索
        judge_num_list = judge_overlap()
        all_node = mk_all_node()

        # 中継器に黒丸を描く
        for point in all_node:
            folium.Circle(location=get_gps(point), radius=12, color = "black", fill = True).add_to(folium_map)

        # 各センサからの使用経路を描く
        for set in [("blue", 3),("#FF7E00", 7)]:
            color, loc_num = set

            try:
                route = mk_route(loc_num)

                # 重なっている経路の片方をずらして描く
                if loc_num in judge_num_list:
                    for loc in route:
                        folium.PolyLine(locations = [np.float_(get_gps(loc[0]))*1.000001, np.float_(get_gps(loc[1]))*1.000001], color = color).add_to(folium_map)
                
                # その他の経路を通常通り描く
                else:
                    for loc in route:
                        folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = color).add_to(folium_map)
                # センサの円を描く
                folium.Circle(location=get_gps(loc_num), radius=15, color = color, fill = True).add_to(folium_map)

                # タイムアウトしたノードにバツを描く
                # for node in timeout_node_list:
                #     #print(f"node={timeout_node_list}")
                #     icon = CustomIcon(icon_image = "./image/batu.png", icon_size = (50, 50), icon_anchor = (25, 25), popup_anchor = (0, 0))
                #     folium.Marker(location=get_gps(node),icon = icon).add_to(folium_map)
                for i in break_esp:
                    break_node=fetch_gps_values(i)
                    print(f"break_node{break_node}")
                    icon = CustomIcon(icon_image = "./image/batu.png", icon_size = (50, 50), icon_anchor = (25, 25), popup_anchor = (0, 0))
                    folium.Marker(location=break_node,icon = icon).add_to(folium_map)

            except:
                pass





    else:
        if location == "トイレA": 
            color, loc_num = "blue", 3
        elif location == "ゴミ箱A": 
            color, loc_num = "#FF7E00", 7
        # elif location == "トイレB": 
        #     color, loc_num = "#FF18B5", 11

        route = mk_route(loc_num)

        # 線を引く
        for loc in route:
            folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = color).add_to(folium_map)

        # 黒丸を描く
        for point in route[:-1]:
            folium.Circle(location=get_gps(point[1]), radius=12, color = "black", fill = True).add_to(folium_map)
        
        # センサーの円を描く
        folium.Circle(location=get_gps(loc_num), radius=15, color = color, fill = True).add_to(folium_map)

        for i in break_esp:
            break_node=fetch_gps_values(i)
            print(f"break_node{break_node}")
            icon = CustomIcon(icon_image = "./image/batu.png", icon_size = (50, 50), icon_anchor = (25, 25), popup_anchor = (0, 0))
            folium.Marker(location=break_node,icon = icon).add_to(folium_map)
        # タイムアウトしたノードにバツを描く
        # for node in timeout_node_list:
        #     icon = CustomIcon(icon_image = "./image/batu.png", icon_size = (50, 50), icon_anchor = (25, 25), popup_anchor = (0, 0))
        #     folium.Marker(location=get_gps(node),icon = icon).add_to(folium_map)
 

    # サーバのアイコンを描く
    icon = CustomIcon(icon_image = "./image/office.png", icon_size = (70, 70), icon_anchor = (35, 35), popup_anchor = (0, 0))
    folium.Marker(location=get_gps(1),icon = icon).add_to(folium_map)

    # 全ての変更をセーブする
    folium_map.save('templates/index.html')
    return render_template('index.html')


#----------------------------------------------------------------------------------------
def check_and_update_database(i):
    # データベースへの接続（データベースが存在しない場合は新規作成）
    conn = sqlite3.connect("./instance/location.db")
    # カーソルオブジェクトの作成
    cursor = conn.cursor()
    if i > 0:
        cursor.execute('SELECT id FROM breakesp WHERE id=?', (i,))
        if cursor.fetchone():
            print(f"この{i}は壊れたままです")
        else:
            cursor.execute('INSERT INTO breakesp (id) VALUES (?)', (i,))
            conn.commit()
            print(f"{i}を追加しました")
    elif i==0:
        print("壊れた実機はないそうです")
    else:
        abs_i = abs(i)
        cursor.execute('SELECT id FROM breakesp WHERE id=?', (abs_i,))
        if cursor.fetchone():
            cursor.execute('DELETE FROM breakesp WHERE id=?', (abs_i,))
            conn.commit()
            print(f"{abs_i}を削除しました")
        else:
            print(f"{i}は壊れたという報告は来てません")
    conn.close()



@app.route('/data', methods=['POST','GET'])
def receive_data():
    global route_id, table
    print("-----------------------------------------------------------------------------")
    data = request.get_json()  # 受信したJSONデータを取得
    #data={"message":"5_40"}
    data = data.get('message', '')
    print(f"dataget={data}")

    dtci = re.findall(r"\d+", data)
    print(f"dtci={dtci}")
    print(len(dtci))
    if len(dtci)>3:

        split_data = data.split("_")
        print(split_data)
        if int(split_data[-1]) == 0:
            print("send_back")
            print(split_data)
            routing_table = mk_routing_table()
            print(routing_table)
    
            for one_table in routing_table:
                if int(one_table[0].split("_")[0]) == int(split_data[0]):
                    print("redirect")
                    print(one_table)
                    table = one_table
                    #return redirect(url_for("send_to_esp", parameter = one_table))
                    return table
                
        else:
            # existing_route = route.query.filter_by(route=data).first()

            # if existing_route:
            #     db.session.delete(existing_route)
            #     db.session.commit()

            route_id += 1
            new_route = route(id = route_id,route=data)
            db.session.add(new_route)
            db.session.commit()
        
    else:
        try:
            if int(dtci[0])==3:
                dtci[0]=1
            elif int(dtci[0])==11:
                dtci[0]=2
            elif int(dtci[0])==7:
                dtci[0]=3
            #print(f"吉野の担当：{dtci}")
            
            import time

            # 現在のローカル時間を取得
            local_time = time.localtime()

            # 年月日と時間を整形
            formatted_date = time.strftime("%Y%m%d", local_time)
            formatted_hour = time.strftime("%H%M%S", local_time)

            # リストに格納
            rea = [formatted_date, formatted_hour]
            #print(f"吉野の担当：{rea}")
            
            # データベースへの接続（データベースが存在しない場合は新規作成）
            conn = sqlite3.connect("./instance/location.db")
            # カーソルオブジェクトの作成
            c = conn.cursor()
            
            
            # 同じIDのデータがすでに存在する場合、それを削除
            c.execute("DELETE FROM sensor WHERE id = ?", (dtci[0],))

            # 新しいデータを挿入
            c.execute("INSERT INTO sensor VALUES (?, ?, ?, ?)", (dtci[0], dtci[1], rea[0], rea[1]))

            # 変更をコミット（保存）
            conn.commit()
            
            # 接続を閉じる
            conn.close()
            
            try:
                check_and_update_database(int(dtci[2]))
            except:
                pass
        except:
            print(f"やってきたデータになんらかの不具合があります。該当データ：{dtci}")
        #return render_template('useryoyogi.html')
        # クライアントにデータを送信
    #print("更新するはずなんだ")
    socketio.emit('update_data', {'data': 'your_data_here'})
    return 'Data received successfully'



@app.route('/send_to_esp', methods=['GET','POST'])
def send():
    global send_list, res, table
    send_list = table
    print(send_list)
    data = pickle.dumps(send_list)
    print(data)
    if request.method == 'POST':
        res = request.get_json()
        res = str(res["sign"])
        print(res)
    send_list = []
    return {"routedata": str(data)}


@app.route('/delete')
def delete():
    global route_id
    route_id = 0
    posts = route.query.all()

    for post in posts:
        db.session.delete(post)
        db.session.commit()

    conn = sqlite3.connect("./instance/location.db")
    c = conn.cursor()
    c.execute("DROP TABLE breakesp")
    try:
        c.execute('''CREATE TABLE breakesp (id text)''')
    except:
        pass

    conn.commit()
    conn.close()

    return "deleteed"



"""ここから利用者"""

def resp(text,toileta_num,garbage_num,toiletb_num):
    #print(f"これが知りたいのさ{text,toileta_num,garbage_num,toiletb_num}")
    global TOILETA,GARBAGE,TOILETB
    if text!=[]and text[0]!="":
        if int(text[0])>=50 and int(text[0])<100:
            TOILETA=1
        elif int(text[0])>=100:
            TOILETA=2
        else:
            TOILETA=0
        toileta_num=int(text[0])
    if text[1]!="":
        if int(text[1])>=50 and int(text[1])<100:
            TOILETB=1
        elif int(text[1])>=100:
            TOILETB=2
        else:
            TOILETB=0
        toiletb_num=int(text[1])
    if len(text)>=2:
        if text[2]!="":
            text[2]=str(round(int(text[2])/4))
            #print(f"これが知りたいのさ２{text[2]}")
            if int(text[2])>=30 and int(text[2])<70:
                GARBAGE=1
            elif int(text[2])>=70 and int(text[2])<100:
                GARBAGE=2
            elif int(text[2])>=100:
                GARBAGE=3
            else:
                GARBAGE=0
            garbage_num=int(text[2])
    return toileta_num,toiletb_num,garbage_num

def datetime_now():
    sensors=Sensor.query.all()
    sensors_datetime=[sensors[0].date+sensors[0].time,sensors[1].date+sensors[1].time,sensors[2].date+sensors[2].time]
    date_string=max(sensors_datetime)
    # 日付と時間をパース
    dt = datetime.strptime(date_string, "%Y%m%d%H%M%S")

    # 日付と時間を所望の形式で出力
    dt_now = dt.strftime("%Y年%m月%d日%H時%M分%S秒")
    
    return dt_now
    #print(dt_now)
    
def reset_toilet(resetlis,text,reseta,resetb):
    sensors = Sensor.query.all() # idでエントリを取得
    print(f"resetlis={resetlis}")
    if resetlis[0]!=[]:
        #PARA[0]=str(int(PARA[0])-int(reseta))
        print(f"sensors={sensors}")
        for sensor in sensors:
            if sensor.id =="1":
                reseta=sensors[0].val
                #sensors[0].val="0"
    # else:
    #     for sensor in sensors:
    #         if sensor.id =="1":
    #             sensors[0].val=str(int(PARA[0])-int(reseta))

                
        #text[0]="0"
    if resetlis[1]!=[]:
        #PARA[1]=str(int(PARA[1])-int(resetb))
        for sensor in sensors:
            if sensor.id =="2":
                resetb=sensors[1].val
                #sensors[1].val="0"
    # else:
    #     for sensor in sensors:
    #         if sensor.id =="2":
    #             sensors[1].val=str(int(PARA[1])-int(resetb))
                
        #text[1]="0"
    #print(f"textlis={text}")
    #resetlis=[[], [], '']
    db.session.commit()  # データベースに変更をコミット
    sensors=Sensor.query.all()
    for sensor in sensors:
        if sensor.id =="1":
            sensor_vals1=str(int(sensor.val)-int(reseta))
        elif sensor.id =="2":
            sensor_vals2=str(int(sensor.val)-int(resetb))
        elif sensor.id =="3":
            sensor_vals3=sensor.val
    text=[sensor_vals1,sensor_vals2,sensor_vals3]
    return text,resetlis,reseta,resetb


@app.route('/',methods=['GET','POST'])
def usermap():
    global TOILETA,GARBAGE,TOILETB,PARA,RESETA,RESETB,reseta,resetb
    dt_now = datetime_now()
    toileta_num=0
    toiletb_num=0
    garbage_num=0
    sensors=Sensor.query.all()

    for sensor in sensors:
        if sensor.id =="1":
            #print(f"お試し：id: {sensor.id}, val: {sensor.val}, date: {sensor.date}, time: {sensor.time}")
            sensor_vals1=sensor.val
            #print(sensor_vals1)
        elif sensor.id =="2":
            sensor_vals2=sensor.val
        elif sensor.id =="3":
            sensor_vals3=sensor.val
        print(f"id: {sensor.id}, val: {sensor.val}, date: {sensor.date}, time: {sensor.time}")
    PARA=[sensor_vals1,sensor_vals2,sensor_vals3]
    #print(f"例えば君が{PARA}")
    reset = [request.form.getlist('reseta'),request.form.getlist('resetb'),request.form.get('resetp')]
    PARA,reset,reseta,resetb=reset_toilet(reset,PARA,reseta,resetb)
    
    print(f"例えば君が{PARA,reseta,resetb}")
    print(f"なぜこうなった{reset}")
    #print(f"へぇ{reset,PARA}")
    #text = request.form.getlist('item')
    toileta_num,toiletb_num,garbage_num=resp(PARA,toileta_num,toiletb_num,garbage_num)
    #print(toileta_num)
    

    if request.method == 'GET':
        loca_yoyogi = "ALL"
        return render_template('useryoyogi.html',indextoa_res=toileta_num,indextob_res=toiletb_num,indexga_res=garbage_num,loca_yoyogi=loca_yoyogi,dt_now=dt_now)
    
    else:
        if request.form.get("ubtn", None) != None:
            loca_yoyogi = request.form.get("ubtn", None)
        else:
            loca_yoyogi="ALL"
        #print(f"なぜ{loca_yoyogi}")
        return render_template('useryoyogi.html',indextoa_res=toileta_num,indextob_res=toiletb_num,indexga_res=garbage_num,loca_yoyogi=loca_yoyogi,dt_now=dt_now)
    
@app.route('/#info-1',methods=['GET','POST'])
def resetmap():
    #print("Hey")
    usermap()

@app.route('/<loca_yoyogi>',methods = ["GET"])
def userfoliummap(loca_yoyogi):
    global TOILETA,GARBAGE,TOILETB
    toilet_sum=0
    start_cords=(35.67061628919986, 139.69567437962016)
    folium_map = folium.Map(location=start_cords, zoom_start=16)



    gps_group = []
    ins_group = []
    posts = Post.query.all()
    #print(f"どうどう{posts[0]}")

    for post in posts:
        #print(f"どうどう{db.Model}")
        gps_group.append(post.gps.split(","))
        ins_group.append(post.ins)
    for ins in range(len(ins_group)):
        if ins_group[ins] =="toilet":
            if toilet_sum==0:
                ins_group[ins] ="toileta"
                toilet_sum+=1
            elif toilet_sum==1:
                ins_group[ins] ="toiletb"
                toilet_sum+=1
    #print(loca_yoyogi)


    for gps, ins in zip(gps_group, ins_group):
        
        #print(f"どうどう{gps,ins}")
        if ins == "toileta":
            if loca_yoyogi=="ALL" or loca_yoyogi=="トイレA" :
                if TOILETA==0 :
                    icon_image = "./image/toilet_b.png"
                elif TOILETA==1 :
                    icon_image = "./image/toilet_o.png"
                elif TOILETA==2:
                    icon_image = "./image/toilet_r.png"
            else:
                icon_image = "./image/zero.png"
        elif ins == "toiletb":
            pass
            # if loca_yoyogi=="ALL" or loca_yoyogi=="トイレB" :
            #     if TOILETB==0 :
            #         icon_image = "./image/toilet_b.png"
            #     elif TOILETB==1 :
            #         icon_image = "./image/toilet_o.png"
            #     elif TOILETB==2:
            #         icon_image = "./image/toilet_r.png"
            # else:
            #     icon_image = "./image/zero.png"

        elif ins == "box":
            if loca_yoyogi=="ALL" or loca_yoyogi=="ゴミ箱A" :
                if GARBAGE==0:
                    icon_image = "./image/box_b.png"
                elif GARBAGE==1:
                    icon_image = "./image/box_o.png"
                elif GARBAGE==2:
                    icon_image = "./image/box_r.png"
                elif GARBAGE==3:
                    pass
                else:
                    icon_image = "./image/zero.png"
            if GARBAGE==3:
                icon_image = "./image/box_r.png"
        elif ins == "office":
            icon_image = "./image/zero.png"
        # else:
        #     icon_image = "./image/black.png"
        else:
            icon_image = "./image/zero.png"
        


        icon = CustomIcon(
            icon_image = icon_image
            ,icon_size = (50, 50)
            ,icon_anchor = (30, 30)
            ,popup_anchor = (0, 0)
            )
        folium.Marker(location=gps,icon = icon).add_to(folium_map)
        
        #folium.Marker(location=gps,icon = icon).add_to(folium_map)

    folium_map.save('templates/yoyogimap.html')
    return render_template('yoyogimap.html')



if __name__ == "__main__":
    #app.run(debug=False ,host='0.0.0.0', port=80)
    #app.run(debug=True, host='0.0.0.0', port=5000)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
