import folium
from flask import Flask,render_template,request,redirect
from folium.features import CustomIcon
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import datetime
TOILETA=0
GARBAGE=0
TOILETB=0




app = Flask(__name__)
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
    
    
"""ここからログイン"""
@app.route('/',methods=['GET','POST'])
def map():
    text = request.form.getlist('username')
    print(text)
    return render_template('login.html')


    


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
                    if int(plus_tabele[0].split("_")[-1]) > int(post.route.split("_")[0]):
                        plus_tabele.insert(0, post.route)
                    else:
                        plus_tabele.append(post.route)
                else:
                    plus_tabele.append(post.route)
        routing_table.append(plus_tabele)
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
        if int(post.id) == num:
            return post.gps.split(",")

#numのgpsナンバーを返答
def get_num_gps(num):
    posts = Post.query.all()
    for post in posts:
        if post.id == num:
            return post.num_gps.split(",")

#numのespを返答
def get_ins(num):
    posts = Post.query.all()
    for post in posts: 
        if post.id == num:
            return post.ins

#numのespの名前を返答
def get_ins_name(num):
    posts = Post.query.all()
    for post in posts: 
        if post.id == num:
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

def mk_route_txt(loc):
    route = []
    routes_num = mk_routes_num()
    for route_num in routes_num:
        route_txt = f"{get_ins_name(route_num[0])} : "
        for num in route_num:
            route_txt += str(num)
            if num != 1:
                route_txt += " → "
        route.append(route_txt)

    if loc == "ALL": return route
    elif loc == "トイレA": return [route[0]]
    elif loc == "トイレB": return [route[1]]
    else: return [route[2]]

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

def get_timeout_node(route):
    node_set = set()
    for node_tuple in route:
        for node in node_tuple:
            node_set.add(node)

    timeout_node_list = []
    for i in range(1,12):
        if i not in node_set:
            timeout_node_list.append(i)
    
    return timeout_node_list


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
        route = mk_route_txt(location)
        return render_template('index2.html', location = location, route = route)




@app.route('/map/<location>',methods = ["GET"])
def foliummap(location):
    ## マップ全体の決めごと

    start_cords=(35.67061628919986, 139.69567437962016)             #マップの中心位置
    folium_map = folium.Map(location=start_cords, zoom_start=17)    #マップの倍率
    route, color = mk_all_route(),"gray"                            #ルートに関する代入
    timeout_node_list = get_timeout_node(route)                     #タイムアウトしているノードの特定

    # 灰色の線を描く
    for loc in route:
        folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = "gray").add_to(folium_map)

    # 各ノードの番号スタンプを描く
    for i in range(1,12):
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
        for set in [("blue", 5),("#FF7E00", 9), ("#FF18B5", 11)]:
            color, loc_num = set
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
            for node in timeout_node_list:
                icon = CustomIcon(icon_image = "./image/batu.png", icon_size = (50, 50), icon_anchor = (25, 25), popup_anchor = (0, 0))
                folium.Marker(location=get_gps(node),icon = icon).add_to(folium_map)




    else:
        if location == "トイレA": 
            color, loc_num = "blue", 5
        elif location == "トイレB": 
            color, loc_num = "#FF7E00", 9
        elif location == "ゴミ箱A": 
            color, loc_num = "#FF18B5", 11

        route = mk_route(loc_num)

        # 線を引く
        for loc in route:
            folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = color).add_to(folium_map)

        # 黒丸を描く
        for point in route[:-1]:
            folium.Circle(location=get_gps(point[1]), radius=12, color = "black", fill = True).add_to(folium_map)
        
        # センサーの円を描く
        folium.Circle(location=get_gps(loc_num), radius=15, color = color, fill = True).add_to(folium_map)

        # タイムアウトしたノードにバツを描く
        for node in timeout_node_list:
            icon = CustomIcon(icon_image = "./image/batu.png", icon_size = (50, 50), icon_anchor = (25, 25), popup_anchor = (0, 0))
            folium.Marker(location=get_gps(node),icon = icon).add_to(folium_map)
 

    # サーバのアイコンを描く
    icon = CustomIcon(icon_image = "./image/office.png", icon_size = (70, 70), icon_anchor = (35, 35), popup_anchor = (0, 0))
    folium.Marker(location=get_gps(1),icon = icon).add_to(folium_map)

    # 全ての変更をセーブする
    folium_map.save('templates/index.html')
    return render_template('index.html')





@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()  # 受信したJSONデータを取得

    ##ここで値を返す


    # データの処理
    # ...
    print(data)
    # print("Data received successfully")

    return 'Data received successfully'


"""ここから利用者"""

def resp(text,toileta_num,garbage_num,toiletb_num):
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
    dt_now = datetime.datetime.now()
    dt_now=dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    return dt_now
    #print(dt_now)

@app.route('/useryoyogi',methods=['GET','POST'])
def usermap():
    global TOILETA,GARBAGE,TOILETB
    dt_now=datetime_now()
    toileta_num=0
    toiletb_num=0
    garbage_num=0
    text=["0","70","100"]
    #text = request.form.getlist('item')
    toileta_num,toiletb_num,garbage_num=resp(text,toileta_num,toiletb_num,garbage_num)
    #print(toileta_num)

    if request.method == 'GET':
        loca_yoyogi = "ALL"
        return render_template('useryoyogi.html',indextoa_res=toileta_num,indextob_res=toiletb_num,indexga_res=garbage_num,loca_yoyogi=loca_yoyogi,dt_now=dt_now)
    
    else:
        loca_yoyogi = request.form.get("ubtn", None)
        #print(f"なぜ{loca_yoyogi}")
        return render_template('useryoyogi.html',indextoa_res=toileta_num,indextob_res=toiletb_num,indexga_res=garbage_num,loca_yoyogi=loca_yoyogi,dt_now=dt_now)
    




@app.route('/mapyoyogi/<loca_yoyogi>',methods = ["GET"])
def userfoliummap(loca_yoyogi):
    global TOILETA,GARBAGE,TOILETB
    toilet_sum=0
    start_cords=(35.67061628919986, 139.69567437962016)
    folium_map = folium.Map(location=start_cords, zoom_start=16)



    gps_group = []
    ins_group = []
    posts = Post.query.all()
    #print(f"どうどう{posts}")

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
            if loca_yoyogi=="ALL" or loca_yoyogi=="トイレB" :
                if TOILETB==0 :
                    icon_image = "./image/toilet_b.png"
                elif TOILETB==1 :
                    icon_image = "./image/toilet_o.png"
                elif TOILETB==2:
                    icon_image = "./image/toilet_r.png"
            else:
                icon_image = "./image/zero.png"

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



# @app.route('/delete')
# def delete():
#     posts = Post.query.all()

#     for post in posts:
#         db.session.delete(post)
#         db.session.commit()
#     return redirect('/create')



if __name__ == "__main__":
    app.run(debug=True)
