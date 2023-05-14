from flask_app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_app.models import recipe, user

@app.route("/dashboard")
def dashboard():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    user_from_db = user.User.get_by_id({"id":int(session["logged_in"])})
    all_recipes = recipe.Recipe.get_all_with_creators()
    return render_template("dashboard.html", all_recipes=all_recipes, user=user_from_db) 

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
