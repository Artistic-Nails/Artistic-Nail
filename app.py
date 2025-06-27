from collections import defaultdict
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from werkzeug.security import check_password_hash
from flask_bcrypt import Bcrypt
from mongoload import getProducts, getOrders
from mongo import insert_product, insert_custom_product, upload_image
from check_user import checkUser
from add_user import addUser
from send_message import send_order_whatsapp_message
from classes import User, Admin
import bcrypt as bc
from bson import ObjectId
from pymongo import MongoClient
import random
from bson.errors import InvalidId
import os

def is_valid_objectid(oid):
    try:
        ObjectId(oid)
        return True
    except (InvalidId, TypeError):
        return False

app = Flask(__name__)
app.config["SECRET_KEY"] = "nailart"

login_manager = LoginManager(app)
login_manager.init_app(app)
bcrypt = Bcrypt(app)

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client["ArtisticNails"]
customers = db["Customers"]
admins = db["Admins"]
prods = db["Products"]

settings = db["Settings"]
settings.update_one({"name": "custom_price"}, {"$set": {"value": 150}}, upsert=True)

@login_manager.user_loader
def load_user(user_id):
    admin = admins.find_one({"_id": ObjectId(user_id)})
    if admin:
        return Admin(admin)
    return None

@app.route("/")
def land():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        cart = session["cart"]

        if not (username and email and phone):
            return redirect(url_for("register"))

        user_data = addUser(username, email, phone, address, cart)

        if "error" in user_data:
            return redirect(url_for("register"))
        
        object_ids = [ObjectId(pid) for pid in cart if is_valid_objectid(pid)]
        cart_products = list(db.Products.find({"_id": {"$in": object_ids}}))

        # Format items for the WhatsApp message
        items = []
        for p in cart_products:
            items.append({
                "shape": p.get("shape", ""),
                "design": p.get("design", ""),
                "colour": p.get("colour", ""),
                "price": p.get("price", 0)
            })

        send_order_whatsapp_message(phone_number=phone, order_id=user_data["_id"], customer_name=username, items=items, payment_qr_link="")
        session["cart"] = []

        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        admin = db.Admins.find_one({"email": email})
        if admin and bc.checkpw(password.encode("utf-8"), admin["password"]):
            user = Admin(admin)
            login_user(user)
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/home")
def home():
    all_products = getProducts()
    non_custom_products = [p for p in all_products if p["custom"] != True]
    grouped_products = defaultdict(list)

    for p in non_custom_products:
        colour = p.get("colour", "").capitalize()
        grouped_products[colour].append(p)

    return render_template("home.html", grouped_products=grouped_products)


@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/customer_upload")
def customer_upload():
    return render_template("customer_upload.html")

@app.route("/custom")
def custom():
    session["custom"] = list()
    return render_template("custom.html")

@app.route("/custom_shape", methods=["GET", "POST"])
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
    cart_ids = session.get("cart", [])

    # ✅ Filter only valid ObjectIds
    object_ids = [ObjectId(pid) for pid in cart_ids if is_valid_objectid(pid)]

    cart_products = list(db.Products.find({"_id": {"$in": object_ids}}))

    return render_template("checkout.html", products=cart_products, is_cart_empty = len(cart_products) == 0)

@app.route("/admin")
@login_required
def admin():
    orders = getOrders()
    orders = len(orders)
    products = getProducts()
    products = len(products)
    return render_template('admin.html', orders=orders, products=products)


@app.route("/see_orders")
@login_required
def see_orders():
    orders_cursor = db.Customers.find()
    orders = []

    for order in orders_cursor:
        cart_ids = order.get("cart", [])
        product_objects = []

        if cart_ids:
            object_ids = [ObjectId(pid) for pid in cart_ids if is_valid_objectid(pid)]
            product_cursor = db.Products.find({"_id": {"$in": object_ids}})
            product_objects = list(product_cursor)

        order["products"] = product_objects
        orders.append(order)

    return render_template("orders.html", orders=orders)

@app.route("/products")
@login_required
def products():
    products = getProducts()
    return render_template('products.html', products=products)

@app.route("/change_price")
@login_required
def change_price():
    return render_template("change_price.html")

@app.route("/add_to_wishlist")
def add_to_wishlist():
    pid = request.args.get("pid")

    if not pid:
        return redirect(url_for("home"))

    user_id = current_user.id
    user_doc = customers.find_one({"_id": ObjectId(user_id)})

    if user_doc:
        wishlist = user_doc.get("wishlist", [])
        if pid not in wishlist:
            wishlist.append(pid)
            customers.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"wishlist": wishlist}}
            )

    return redirect(url_for("home"))

@app.route("/remove_from_wishlist", methods=["POST"])
def remove_from_wishlist():
    pid = request.args.get("pid")
    if pid:
        customers.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$pull": {"wishlist": pid}}
        )
    return redirect(url_for("wishlist"))

@app.route("/add_to_cart")
def add_to_cart():
    pid = request.args.get("pid")
    if not pid:
        return redirect(url_for("home"))

    if current_user.is_authenticated:
        user_id = current_user.id
        user_doc = customers.find_one({"_id": ObjectId(user_id)})

        cart = user_doc.get("cart", [])
        if pid not in cart:
            cart.append(pid)
            customers.update_one({"_id": ObjectId(user_id)}, {"$set": {"cart": cart}})
    else:
        if "cart" not in session:
            session["cart"] = []

        if pid not in session["cart"]:
            session["cart"].append(pid)
            session.modified = True

    return redirect(url_for("home"))

@app.route("/remove_from_cart")
def remove_from_cart():
    pid = request.args.get("pid")
    if not pid:
        return redirect(url_for("checkout"))

    if current_user.is_authenticated:
        customers.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$pull": {"cart": pid}}
        )
    else:
        if "cart" in session and pid in session["cart"]:
            session["cart"].remove(pid)
            session.modified = True

    return redirect(url_for("checkout"))

@app.route("/remove_product")
@login_required
def remove_product():
    pid = request.args.get("pid")
    if pid:
        pid = ObjectId(pid)
        prods.delete_one({"_id": pid})

    return redirect(url_for("products"))

@app.route("/add_product", methods=["POST", "GET"])
@login_required
def add_product():
    shape = request.form.get("shape")
    colour = request.form.get("colour")
    design = request.form.get("design")
    price = request.form.get("price")
    image = request.files.get("image")

    if shape and colour and design and price and image:
        insert_product(shape, colour, design, price, image)

    return redirect(url_for("products"))

@app.route('/save_shape', methods=['GET', 'POST'])
def save_shape():
    selected_shape = request.form.get('selected_shape')
    print(selected_shape)
    session["custom"] = {}
    session["custom"]["shape"] = selected_shape
    session.modified = True

    return redirect(url_for('custom_colour'))

@app.route('/save_colour', methods=['GET', 'POST'])
def save_colour():
    selected_colour = request.form.get('selected_shape')
    session["custom"]["colour"] = selected_colour
    session.modified = True

    return redirect(url_for("custom_finish"))

@app.route('/add_custom')
def add_custom():
    custom_products = session["custom"]
    insert_custom_product(custom_products["shape"], custom_products["colour"], price=get_custom_price())
    return redirect(url_for("custom_finish"))

@app.route("/add_custom_cart")
def add_custom_cart():
    custom_products = session["custom"]
    pid = insert_custom_product(custom_products["shape"], custom_products["colour"], price=get_custom_price())

    return redirect(url_for("add_to_cart", pid=pid))

@app.route('/complete_order', methods=["GET", "POST"])
def complete_order():
    pid = request.args.get("pid")
    if pid:
        pid = ObjectId(pid)
        customers.delete_one({"_id": pid})

    return redirect(url_for("see_orders"))

@app.route('/surprise_me')
def surprise():
    shapes = ["stiletto", "round", "almond", "ballerina", "square", "coffin"]
    colours = ["red", "blue", "green", "pink", "purple", "yellow"]
    session["custom"] = {"shape": random.choice(shapes), "colour": random.choice(colours)}
    session.modified = True
    custom_products = session["custom"]
    pid = insert_custom_product(custom_products["shape"], custom_products["colour"], price=get_custom_price())

    return redirect(url_for("add_to_cart", pid=pid))

@app.route("/custom_order", methods=["GET", "POST"])
def custom_order():
    shape = request.form.get("shape")
    design = request.form.get("design")
    colour = request.form.get("colour")
    image = request.files.get("image")

    if shape and design and colour and image:
        pid = insert_custom_product(shape, colour, design, upload_image(image), price=get_custom_price())
        return redirect(url_for('add_to_cart', pid=pid))
    
    return redirect(url_for('customer_upload'))

@app.route("/add_custom_instructions", methods=["GET", "POST"])
def add_custom_instructions():
    ins = request.form.get("instructions")
    session["custom"]["instructions"] = ins
    session.modified = True
    custom_products = session["custom"]
    pid = insert_custom_product(custom_products["shape"], custom_products["colour"], instructions=custom_products["instructions"], price=get_custom_price())

    return redirect(url_for("add_to_cart", pid=pid))


@app.route("/set_custom_price", methods=["POST"])
@login_required
def set_custom_price():
    try:
        new_price = float(request.form.get("price"))
        db.Settings.update_one({"name": "custom_price"}, {"$set": {"value": new_price}}, upsert=True)
    except (ValueError, TypeError):
        flash("Invalid price", "error")
    return redirect(url_for('admin'))

# Function to get latest price
def get_custom_price():
    doc = db.Settings.find_one({"name": "custom_price"})
    return doc["value"] if doc else 150

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        app.run(port=5000, debug=True)