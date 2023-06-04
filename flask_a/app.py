import folium
from flask import Flask,render_template,request,redirect
from folium.features import CustomIcon
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import itertools

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location.db'

db = SQLAlchemy(app) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gps = db.Column(db.Integer, nullable=True)
    num_gps = db.Column(db.Integer)
    ins = db.Column(db.String(100))
    esp_name = db.Column(db.String(100))


line_all = [(9,10),(9,7),(10,7),(10,11),(11,8),(11,7),(7,5),(8,4),(4,1),(2,1),(5,2),(7,8),(6,5),(6,7),(6,10),(6,9)  ,(3,1),(7,3),(6,3),(8,3),(5,3)]
all_node = [2,3,4,6,7,8,10]
routes_num = [(5,3,1),(11,8,4,1),(9,7,3,1)]


def get_gps(num):
    posts = Post.query.all()
    for post in posts: 
        if post.id == num:
            return post.gps.split(",")

def get_num_gps(num):
    posts = Post.query.all()
    for post in posts: 
        if post.id == num:
            return post.num_gps.split(",")

def get_ins(num):
    posts = Post.query.all()
    for post in posts: 
        if post.id == num:
            return post.ins

def get_ins_name(num):
    posts = Post.query.all()
    for post in posts: 
        if post.id == num:
            return post.esp_name

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
    for route in routes_num:
        route_list.append(mk_route(route[0]))

    judge_num_list = []
    for pair in itertools.combinations(route_list, 2):
        if set(pair[0])&set(pair[1]):
            judge_num_list.append(pair[0][0][0])    
    return judge_num_list

def get_timeout_node():
    node_set = set()
    for node_tuple in line_all:
        for node in node_tuple:
            node_set.add(node)

    timeout_node_list = []
    for i in range(1,12):
        if i not in node_set:
            timeout_node_list.append(i)
    
    return timeout_node_list


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
    timeout_node_list = get_timeout_node()
    route, color, loc_num = line_all,"gray",0

    for loc in line_all:
        folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = "gray").add_to(folium_map)

    for i in range(1,12):
        a = f"./image/num{i}.png"
        icon = CustomIcon(icon_image = a, icon_size = (60, 55), icon_anchor = (35, 35), popup_anchor = (0, 0))
        folium.Marker(location=get_num_gps(i),icon = icon).add_to(folium_map)

    if location == "ALL":
        judge_num_list = judge_overlap()

        for point in all_node:
            folium.Circle(location=get_gps(point), radius=12, color = "black", fill = True).add_to(folium_map)

        for set in [("blue", 5),("#FF7E00", 9), ("#FF18B5", 11)]:
            color, loc_num = set
            route = mk_route(loc_num)

            if loc_num in judge_num_list:
                for loc in route:
                    folium.PolyLine(locations = [np.float_(get_gps(loc[0]))*1.000001, np.float_(get_gps(loc[1]))*1.000001], color = color).add_to(folium_map)
            else:
                for loc in route:
                    folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = color).add_to(folium_map)

            folium.Circle(location=get_gps(loc_num), radius=15, color = color, fill = True, ).add_to(folium_map)

            for node in timeout_node_list:
                icon = CustomIcon(icon_image = "./image/batu.png", icon_size = (50, 50), icon_anchor = (25, 25), popup_anchor = (0, 0))
                folium.Marker(location=get_gps(node),icon = icon).add_to(folium_map)

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
 

    icon = CustomIcon(icon_image = "./image/office.png", icon_size = (70, 70), icon_anchor = (35, 35), popup_anchor = (0, 0))
    folium.Marker(location=get_gps(1),icon = icon).add_to(folium_map)

    folium_map.save('templates/index.html')
    return render_template('index.html')



@app.route("/create", methods = ["POST", "GET"])
def a():
    if request.method == 'GET':
        return render_template('index3.html')

    else:
        gps = request.form.get('gps')
        num_gps = request.form.get("num_gps")
        ins = request.form.get('ins')
        esp_name = request.form.get("esp_name")
            
        new_post = Post(gps = gps, num_gps = num_gps, ins = ins, esp_name = esp_name)

        db.session.add(new_post)
        db.session.commit()
        return redirect("/create")
    
@app.route('/delete')
def delete():
    post = Post.query.all()

    for i in post:
        db.session.delete(i)
        db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
