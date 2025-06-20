from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_dict):
        self.id = str(user_dict["_id"])  # Required for Flask-Login
        self.username = user_dict.get("username")
        self.email = user_dict.get("email")
        self.address = user_dict.get("address")
        self.wishlist = user_dict.get("wishlist")
        self.cart = user_dict.get("cart")

        # You can add more attributes as needed
        self.mongo_user = user_dict  # keep full original dict if needed


class Admin(UserMixin):
    def __init__(self, admin_dict):
        self.id = str(admin_dict["_id"])
        self.email = admin_dict["email"]