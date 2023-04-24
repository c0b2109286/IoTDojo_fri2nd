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

@app.route('/admin')
def route():
    posts = Post.query.all()
    return render_template('index2.html', posts = posts)

@app.route('/map',methods = ["GET", "POST"])
def foliummap():
    global First_round
    start_cords=(35.67061628919986, 139.69567437962016)
    folium_map = folium.Map(location=start_cords, zoom_start=17)

    gps_group = []
    posts = Post.query.all()

    for post in posts:
        gps_group.append(post.gps.split(","))

    if request.method == 'GET':
        print("GET")
        return render_template('index.html')

    
    else:
        print("POST")
        value = request.form.get("btn", None)
        if value == "ALL":
            for loc in line:
                folium.PolyLine(locations = [np.float_(gps_group[loc[0]-1]), np.float_(gps_group[loc[1]-1])], color = "gray").add_to(folium_map)
        elif value == "ログアウト":
            return redirect("/map")

        folium_map.save('templates/index.html')
        return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)