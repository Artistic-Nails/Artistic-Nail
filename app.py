from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from werkzeug.security import check_password_hash
from flask_bcrypt import Bcrypt
from mongoload import getProducts, getOrders
from mongo import insert_product, insert_custom_product
from check_user import checkUser
from add_user import addUser
from classes import User, Admin
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

uri = "mongodb+srv://artisticnailsbyharman:QLbPCWSz9VHKnO3t@cluster0.mbnwbwo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["ArtisticNails"]
customers = db["Customers"]
admins = db["Admins"]
prods = db["Products"]

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
            flash("Please fill in all fields", "danger")
            return redirect(url_for("register"))

        user_data = addUser(username, email, phone, address, cart)

        if "error" in user_data:
            flash(user_data["error"], "danger")
            return redirect(url_for("register"))

        user = User(user_data)
        login_user(user)
        flash("Registration successful!", "success")
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
            flash("Logged in as admin", "success")
            return redirect(url_for("admin"))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/home")
def home():
    products = getProducts()
    return render_template("home.html", products=products)

@app.route("/wishlist")
def wishlist():
    user_id = current_user.id
    user_doc = customers.find_one({"_id": ObjectId(user_id)})

    wishlist_ids = user_doc.get("wishlist", [])

    object_ids = [ObjectId(pid) for pid in wishlist_ids]

    wishlist_products = db.Products.find({"_id": {"$in": object_ids}})
    print(wishlist_products)
    return render_template("wishlist.html", products=wishlist_products)

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
    if current_user.is_authenticated:
        cart_ids = customers.find_one({"_id": ObjectId(current_user.id)}).get("cart", [])
    else:
        cart_ids = session.get("cart", [])

    object_ids = [ObjectId(pid) for pid in cart_ids]
    cart_products = db.Products.find({"_id": {"$in": object_ids}})

    return render_template("checkout.html", products=cart_products)

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
            object_ids = [ObjectId(pid) for pid in cart_ids]
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

@app.route("/add_to_wishlist")
def add_to_wishlist():
    pid = request.args.get("pid")

    if not pid:
        flash("Invalid product ID", "danger")
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
            flash("Added to wishlist", "success")
        else:
            flash("Already in wishlist", "info")
    else:
        flash("User not found", "danger")

    return redirect(url_for("home"))

@app.route("/remove_from_wishlist", methods=["POST"])
def remove_from_wishlist():
    pid = request.args.get("pid")
    if pid:
        customers.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$pull": {"wishlist": pid}}
        )
        flash("Removed from wishlist", "info")
    return redirect(url_for("wishlist"))

@app.route("/add_to_cart")
def add_to_cart():
    pid = request.args.get("pid")
    if not pid:
        flash("Invalid product ID", "danger")
        return redirect(url_for("home"))

    if current_user.is_authenticated:
        # Logged-in user cart in MongoDB
        user_id = current_user.id
        user_doc = customers.find_one({"_id": ObjectId(user_id)})

        cart = user_doc.get("cart", [])
        if pid not in cart:
            cart.append(pid)
            customers.update_one({"_id": ObjectId(user_id)}, {"$set": {"cart": cart}})
            flash("Added to cart", "success")
        else:
            flash("Already in cart", "info")
    else:
        if "cart" not in session:
            session["cart"] = []

        if pid not in session["cart"]:
            session["cart"].append(pid)
            session.modified = True
            flash("Added to cart (guest)", "success")
        else:
            flash("Already in cart (guest)", "info")

    return redirect(url_for("home"))

@app.route("/remove_from_cart")
def remove_from_cart():
    pid = request.args.get("pid")
    if not pid:
        flash("Invalid product ID", "danger")
        return redirect(url_for("checkout"))

    if current_user.is_authenticated:
        # Logged-in user: remove from MongoDB cart
        customers.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$pull": {"cart": pid}}
        )
        flash("Removed from cart", "info")
    else:
        # Guest user: remove from session cart
        if "cart" in session and pid in session["cart"]:
            session["cart"].remove(pid)
            session.modified = True
            flash("Removed from cart (guest)", "info")
        else:
            flash("Item not in cart (guest)", "warning")

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
    session["custom"] = {}
    session["custom"]["shape"] = selected_shape

    # Save it to session or DB if needed
    # session['shape'] = selected_shape

    return redirect(url_for('custom_colour'))  # or render a page

@app.route('/save_colour', methods=['GET', 'POST'])
def save_colour():
    selected_colour = request.form.get('selected_shape')
    print("User selected colour:", selected_colour)
    session["custom"]["colour"] = selected_colour
    print(session["custom"])
    session.modified = True

    # Save it to session or DB if needed
    # session['shape'] = selected_shape

    return redirect(url_for('custom_finish'))  # or render a page

@app.route('/add_custom')
def add_custom():
    custom_products = session["custom"]
    insert_custom_product(custom_products["shape"], custom_products["colour"])
    return redirect(url_for("custom_finish"))

@app.route("/add_custom_cart")
def add_custom_cart():
    custom_products = session["custom"]
    pid = insert_custom_product(custom_products["shape"], custom_products["colour"])

    return redirect(url_for("add_to_cart", pid=pid))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        app.run(port=5000, debug=True)