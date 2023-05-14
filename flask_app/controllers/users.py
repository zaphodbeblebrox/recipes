from flask_app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models import user
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    if "logged_in" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html") 

@app.route("/register", methods=["POST"])
def register():
    if not user.User.is_valid(request.form):
        return redirect(url_for("index"))
    else:
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form["password"])
        }
        user.User.create(data)
        flash("Account Created, please login.")
        return redirect(url_for("index"))
    
@app.route("/login_form")
def login_form():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = {
        "email": request.form["email"]
    }
    user_from_db = user.User.get_by_email(data)
    
    if not user_from_db:
        flash("Invalid login")
        return redirect(url_for("index"))
    if not bcrypt.check_password_hash(user_from_db.password, request.form["password"]):
        flash("Invalid login")
        return redirect(url_for("index"))
    
    session["logged_in"] = user_from_db.id
    return redirect(url_for("dashboard"))
