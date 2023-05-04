import folium
from flask import Flask,render_template,request,redirect
from folium.features import CustomIcon
from flask_sqlalchemy import SQLAlchemy
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location.db'
db = SQLAlchemy(app) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gps = db.Column(db.Integer, nullable=True)
    ins = db.Column(db.String(100))


line = [(9,10),(9,7),(10,7),(10,11),(11,8),(11,7),(7,3),(7,5),(8,3),(5,3),(8,4),(4,1),(3,1),(2,1),(5,2),(7,8)  ,(6,5),(6,3),(6,7),(6,10),(6,9)]
routes_num = [(5,3,1),(11,8,4,1),(9,6,7,3,1)]


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
        route = mk_route_txt(location)
        return render_template('index2.html', location = location, route = route)




@app.route('/map/<location>',methods = ["GET"])
def foliummap(location):
    start_cords=(35.67061628919986, 139.69567437962016)
    folium_map = folium.Map(location=start_cords, zoom_start=17)

    if location == "ALL":
        for loc in line:
            folium.PolyLine(locations = [np.float_(get_gps(loc[0])), np.float_(get_gps(loc[1]))], color = "gray").add_to(folium_map)

    folium_map.save('templates/index.html')
    return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True)
