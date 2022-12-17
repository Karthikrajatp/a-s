from flask import Flask,render_template,redirect,url_for,request
from flask_admin import AdminIndexView
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
DB_NAME="database.db"

class Dog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    dogname = db.Column(db.String(100))
    ownername = db.Column(db.String(100))
    dogbreed = db.Column(db.String(100))
    owneremail = db.Column(db.String(100))
    dogcity = db.Column(db.String(100))
    dogpincode = db.Column(db.String(100))

app = Flask(__name__)
app.config['SECRET_KEY']="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
app.config['SQLALCHEMY_DATABASE_URI']=f"sqlite:///{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/',methods=['POST','GET'])
@app.route('/home',methods=['POST','GET'])
def home():
    return render_template("home.html")


@app.route('/adddog',methods=['POST','GET'])
def adddog():
    if request.method == "POST":
        dogname=request.form.get('name')
        ownername = request.form.get('ownername')
        dogbreed = request.form.get('breed')
        owneremail = request.form.get('email')
        dogcity = request.form.get('city')
        dogpincode = request.form.get('pincode')
        new_dog = Dog(dogname=dogname,ownername=ownername,dogbreed=dogbreed,owneremail=owneremail,dogcity=dogcity,dogpincode=dogpincode)
        db.session.add(new_dog)
        db.session.commit()
        return redirect("/home")
    return render_template("adddog.html")

@app.route('/searchdog',methods=['POST','GET'])
def searchdog():
    if request.method=="GET":
        pincode = request.args.get("pincodesearch")
        city = request.args.get("citysearch")
        if(pincode and city):
            dogs=Dog.query.filter(Dog.dogpincode.like('%'+pincode+'%'),Dog.dogcity.like('%'+city+'%')).all()
            return render_template("search.html",dogs=dogs)
        elif(pincode and not(city)):
            dogs=Dog.query.filter(Dog.dogpincode.like('%'+pincode+'%')).all()
            return render_template("search.html",dogs=dogs)
        elif(not(city) and pincode):
            dogs=Dog.query.filter(Dog.dogcity.like('%'+city+'%')).all()
            return render_template("search.html",dogs=dogs)
        else:
            return render_template("search.html")
    else:
        return render_template("search.html")



if __name__=="__main__":
    app.run(debug=True)