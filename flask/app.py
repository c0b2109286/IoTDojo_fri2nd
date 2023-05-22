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
    ins = db.Column(db.String(100))
    
    
"""ここからログイン"""
@app.route('/',methods=['GET','POST'])
def map():
    text = request.form.getlist('username')
    print(text)
    return render_template('login.html')


    


"""ここから管理者"""
line_all = [(9,10),(9,7),(10,7),(10,11),(11,8),(11,7),(7,3),(7,5),(8,3),(5,3),(8,4),(4,1),(3,1),(2,1),(5,2),(7,8)  ,(6,5),(6,3),(6,7),(6,10),(6,9)]
all_node = [2,3,4,6,7,8,10]
routes_num = [(5,2,1),(11,8,4,1),(9,6,7,3,1)]


def get_gps(num):
    posts = Post.query.all()
    for post in posts: 
        if post.id == num:
            return post.gps.split(",")

def get_ins(num):
    posts = Post.query.all()
    for post in posts: 
        if post.id == num:
            return post.ins
        
def mk_route(num):
    for line in routes_num:
        if line[0] == num:
            route = []
            for i in range(len(line)-1):
                route.append((line[i],line[i+1]))
    return route


def mk_route_txt(loc):
    route = []
    for route_num in routes_num:
        route_txt = f"{get_ins(route_num[0])} : "
        for num in route_num:
            route_txt += str(num)
            if num != 1:
                route_txt += " → "
        route.append(route_txt)

    if loc == "ALL": return route
    elif loc == "トイレA": return [route[0]]
    elif loc == "トイレB": return [route[1]]
    else: return [route[2]]
        


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
    start_cords=(35.67061628919986, 139.69567437962016)
    folium_map = folium.Map(location=start_cords, zoom_start=17)
    route, color, loc_num = line_all,"gray",0

    for loc in line_all:
        folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = "gray").add_to(folium_map)

    if location == "ALL":
        for point in all_node:
            folium.Circle(location=get_gps(point), radius=12, color = "black", fill = True).add_to(folium_map)

        for set in [("blue", 5),("#FF7E00", 9), ("#FF18B5", 11)]:
            color, loc_num = set
            route = mk_route(loc_num)

            for loc in route:
                folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = color).add_to(folium_map)

            folium.Circle(location=get_gps(loc_num), radius=15, color = color, fill = True).add_to(folium_map)

    else:
        if location == "トイレA": color, loc_num = "blue", 5
        elif location == "トイレB": color, loc_num = "#FF7E00", 9
        elif location == "ゴミ箱A": color, loc_num = "#FF18B5", 11

        route = mk_route(loc_num)

        for loc in route:
            folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = color).add_to(folium_map)

        for point in route[:-1]:
            folium.Circle(location=get_gps(point[1]), radius=12, color = "black", fill = True).add_to(folium_map)

        folium.Circle(location=get_gps(loc_num), radius=15, color = color, fill = True).add_to(folium_map)


    icon = CustomIcon(icon_image = "./image/office.png", icon_size = (50, 50), icon_anchor = (25, 25), popup_anchor = (0, 0))
    folium.Marker(location=get_gps(1),icon = icon).add_to(folium_map)

    folium_map.save('templates/index.html')
    return render_template('index.html')


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