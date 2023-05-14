from flask_app import app
from flask import render_template, request, redirect, url_for, flash, session
from flask_app.models.user import User
from flask_app.models import recipe

@app.route("/recipes/new")
def add_recipe():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    return render_template("add_recipe.html")

@app.route("/recipes/process", methods=["POST"])
def create_recipe():
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    if not recipe.Recipe.is_valid(request.form):
        return redirect(url_for("add_recipe"))
    else:
        data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date_cooked": request.form["date_cooked"],
            "under_30_min": request.form["under_30_min"],
            "user_id": int(session['logged_in'])
        }
        recipe.Recipe.create(data)
        return redirect("/dashboard")

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    one_recipe = recipe.Recipe.get_one_with_user({"id": id})
    return render_template("edit_recipe.html", one_recipe=one_recipe)

@app.route("/recipes/update/<int:id>", methods=["POST"])
def update(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    if not recipe.Recipe.is_valid(request.form):
        return redirect(f"/recipes/edit/{id}")
    else:
        data = {
            "id": id,
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date_cooked": request.form["date_cooked"],
            "under_30_min": request.form["under_30_min"],
            "user_id": int(session['logged_in'])
        }
        recipe.Recipe.update(data)
        return redirect("/dashboard")

@app.route("/recipes/<int:id>")
def view_recipe(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    recipe_from_db = recipe.Recipe.get_one_with_user({"id":id})
    user_from_db = User.get_by_id({"id":int(session["logged_in"])})
    return render_template("view_recipe.html", recipe=recipe_from_db, user=user_from_db)

@app.route("/recipes/delete/<int:id>")
def delete(id):
    if "logged_in" not in session:
        flash("You must be logged in to view that page")
        return redirect(url_for("index"))
    recipe.Recipe.destroy({"id":id})
    return redirect(url_for("dashboard"))