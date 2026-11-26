from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User

auth = Blueprint("auth", __name__)

@auth.route("/registro", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated: return redirect(url_for("main.index"))
    if request.method == "POST":
        name, email = request.form.get("name","").strip(), request.form.get("email","").strip().lower()
        password, phone = request.form.get("password",""), request.form.get("phone","").strip()
        if not name or not email or len(password) < 8:
            flash("Completá los datos. La contraseña debe tener al menos 8 caracteres.", "error")
        elif User.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado.", "error")
        else:
            user = User(name=name, email=email, phone=phone)
            user.set_password(password)
            db.session.add(user); db.session.commit()
            login_user(user)
            return redirect(url_for("main.index"))
    return render_template("auth.html", mode="register")

@auth.route("/ingresar", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email","").strip().lower()).first()
        if user and user.check_password(request.form.get("password","")):
            login_user(user)
            return redirect(url_for("admin.dashboard" if user.is_admin else "main.index"))
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("auth.html", mode="login")

@auth.get("/salir")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
