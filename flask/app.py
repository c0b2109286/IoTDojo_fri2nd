## 改良4
import folium
from flask import Flask,render_template,request,redirect
from folium.features import CustomIcon
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location.db'
db = SQLAlchemy(app) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gps = db.Column(db.Integer, nullable=True)
    ins = db.Column(db.String(100))

@app.route('/')
def map():
    return render_template('index2.html')

@app.route('/map',methods = ["GET"])
def foliummap():
    start_cords=(35.67061628919986, 139.69567437962016)
    folium_map = folium.Map(location=start_cords, zoom_start=17)

    gps_group = []
    ins_group = []
    posts = Post.query.all()

    for post in posts:
        gps_group.append(post.gps.split(","))
        ins_group.append(post.ins)

    for gps, ins in zip(gps_group, ins_group):
        if ins == "toilet":
            icon_image = "./image/blue.png"
        elif ins == "box":
            icon_image = "./image/blue.png"
        elif ins == "office":
            icon_image = "./image/office.png"
        else:
            icon_image = "./image/black.png"


        icon = CustomIcon(
            icon_image = icon_image
            ,icon_size = (50, 50)
            ,icon_anchor = (30, 30)
            ,popup_anchor = (0, 0)
            )

        folium.Marker(location=gps,icon = icon).add_to(folium_map)

    folium_map.save('templates/index.html')
    return render_template('index.html')


@app.route("/create", methods = ["POST", "GET"])
def a():
    if request.method == 'GET':
        return render_template('index3.html')

    else:
        gps = request.form.get('gps')
        ins = request.form.get('ins')
            
        new_post = Post(gps = gps, ins = ins)

        db.session.add(new_post)
        db.session.commit()
        return redirect("/create")

@app.route('/delete')
def delete():
    posts = Post.query.all()

    for post in posts:
        db.session.delete(post)
        db.session.commit()
    return redirect('/create')



if __name__ == "__main__":
    app.run(debug=True)

