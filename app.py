from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "kuchtohhaibasye"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:aryan2424@localhost/vidyutam'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)

@app.route("/")
def land():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/wishlist")
def wishlist():
    return render_template("wishlist.html")

if __name__ == "__main__":
    with app.app_context():
        app.run(port=5000, debug=True)