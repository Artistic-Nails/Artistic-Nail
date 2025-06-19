from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from werkzeug.security import check_password_hash
from flask_bcrypt import Bcrypt
from mongoload import getProducts
from check_user import checkUser
import bcrypt as bc
from bson import ObjectId
from pymongo import MongoClient

app = Flask(__name__)
app.config["SECRET_KEY"] = "nailart"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aryan2424@localhost/vidyutam'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager(app)
login_manager.init_app(app)
bcrypt = Bcrypt(app)

client = MongoClient("mongodb+srv://nevarycolab:1F0J6rXtdrC0zi1X@cluster0.ohuk50d.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["nailArt"]
collection = db["Customers"]

@login_manager.user_loader
def load_user(user_id):
    from classes import User  # import the class you created earlier
    user_dict = collection.find_one({"_id": ObjectId(user_id)})
    if user_dict:
        return User(user_dict)
    return None

@app.route("/")
def land():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = checkUser({"email": email})  # your own function to check if user exists
        if user and bc.checkpw(password.encode('utf-8'), user.password):
            login_user(user)  # flask_login method
            print("Logged in successfully", "success")
            return redirect(url_for("home"))
        else:
            print("Invalid email or password", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/home")
def home():
    products = getProducts()
    return render_template("home.html", products=products)

@app.route("/wishlist")
def wishlist():
    return render_template("wishlist.html")

@app.route("/custom")
def custom():
    return render_template("custom.html")

@app.route("/custom_shape")
def custom_shape():
    return render_template("custom-shape.html")

@app.route("/custom_colour")
def custom_colour():
    return render_template("custom-colour.html")

@app.route("/custom_finish")
def custom_finish():
    return render_template("custom-finish.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

if __name__ == "__main__":
    with app.app_context():
        app.run(port=5000, debug=True)