## 改良4
import folium
from flask import Flask,render_template,request,redirect
from folium.features import CustomIcon
from flask_sqlalchemy import SQLAlchemy
import argparse
from config_utils import ConfigUtils

TOILETA=0
GARBAGE=0
TOILETB=0

parser = argparse.ArgumentParser()
parser.add_argument('--config',default='config/config.yaml',type=str)
args = parser.parse_args()

CONFIG_FILEPATH = args.config

def update_notify(yamlfile):
    status = ConfigUtils.load(args.config)['notification']
    if status == "on":
        ConfigUtils.update(args.config,'notification', 'off')
    elif status == "off":
        ConfigUtils.update(args.config,'notification', 'on')
    else:
        raise Exception('Invalid value in yaml file')  

def read_notify(yamlfile):
    config = ConfigUtils.load(args.config)
    return config['notification']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location.db'
db = SQLAlchemy(app) 

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gps = db.Column(db.Integer, nullable=True)
    ins = db.Column(db.String(100))
    
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
            elif int(text[2])>=70:
                GARBAGE=2
            else:
                GARBAGE=0
            garbage_num=int(text[2])
    return toileta_num,toiletb_num,garbage_num

@app.route('/useryoyogi',methods=['GET','POST'])
def map():
    global TOILETA,GARBAGE,TOILETB
    toileta_num=0
    toiletb_num=0
    garbage_num=0
    text=["0","70","100"]
    #text = request.form.getlist('item')
    toileta_num,toiletb_num,garbage_num=resp(text,toileta_num,toiletb_num,garbage_num)
    #print(toileta_num)
    return render_template('index4.html',indextoa_res=toileta_num,indextob_res=toiletb_num,indexga_res=garbage_num)




@app.route('/mapyoyogi',methods = ["GET"])
def foliummap():
    global TOILETA,GARBAGE,TOILETB
    toilet_lis=[TOILETA,TOILETB]
    toilet_num=0
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
        


    for gps, ins in zip(gps_group, ins_group):
        print(f"どうどう{gps,ins}")
        if ins == "toilet":
                if toilet_lis[toilet_num]==0 :
                    icon_image = "./image/toilet_b.png"
                elif toilet_lis[toilet_num]==1 :
                    icon_image = "./image/toilet_y.png"
                elif toilet_lis[toilet_num]==2:
                    icon_image = "./image/toilet_r.png"
                if toilet_num==0:
                    toilet_num=1
                else:
                    toilet_num=0

        elif ins == "box":
            if GARBAGE==0:
                icon_image = "./image/box_b.png"
            elif GARBAGE==1:
                icon_image = "./image/box_y.png"
            elif GARBAGE==2:
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

    folium_map.save('templates/index3.html')
    return render_template('index3.html')

# @app.route('/map',methods = ["GET"])
# def foliummap():
#     start_cords=(35.67061628919986, 139.69567437962016)
#     folium_map = folium.Map(location=start_cords, zoom_start=17)

#     gps_group = []
#     ins_group = []
#     posts = Post.query.all()

#     for post in posts:
#         gps_group.append(post.gps.split(","))
#         ins_group.append(post.ins)

#     for gps, ins in zip(gps_group, ins_group):
#         if ins == "toilet":
#             icon_image = "./image/blue.png"
#         elif ins == "box":
#             icon_image = "./image/black.png"
#         elif ins == "office":
#             icon_image = "./image/office.png"
#         else:
#             icon_image = "./image/black.png"
#         # else:
#         #     icon_image = "./image/zero.png"


#         icon = CustomIcon(
#             icon_image = icon_image
#             ,icon_size = (50, 50)
#             ,icon_anchor = (30, 30)
#             ,popup_anchor = (0, 0)
#             )

#         folium.Marker(location=gps,icon = icon).add_to(folium_map)

#     folium_map.save('templates/index_admin.html')
#     return render_template('index_admin.html')


# @app.route("/create", methods = ["POST", "GET"])
# def a():
#     if request.method == 'GET':
#         return render_template('index.html')

#     else:
#         gps = request.form.get('gps')
#         ins = request.form.get('ins')
            
#         new_post = Post(gps = gps, ins = ins)

#         db.session.add(new_post)
#         db.session.commit()
#         return redirect("/create")

# @app.route('/delete')
# def delete():
#     posts = Post.query.all()

#     for post in posts:
#         db.session.delete(post)
#         db.session.commit()
#     return redirect('/create')



if __name__ == "__main__":
    app.run(debug=True)

