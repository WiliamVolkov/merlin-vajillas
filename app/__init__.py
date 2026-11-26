import os
from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf.init_app(app)

    from app.models import User, Category, Product, RentalRequest, RentalItem
    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.admin import admin
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix="/admin")

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    with app.app_context():
        db.create_all()
        if not Category.query.first():
            for name in ["Vasos", "Copas", "Platos", "Jarras", "Otros"]:
                db.session.add(Category(name=name))
            db.session.commit()
        if not User.query.filter_by(email=os.environ.get("ADMIN_EMAIL", "admin@merlinvajillas.com")).first():
            admin_user = User(name="Administrador", email=os.environ.get("ADMIN_EMAIL", "admin@merlinvajillas.com"), is_admin=True)
            admin_user.set_password(os.environ.get("ADMIN_PASSWORD", "Cambiar123!"))
            db.session.add(admin_user)
            db.session.commit()
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return db.session.get(User, int(user_id))
