from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category, RentalRequest

admin = Blueprint("admin", __name__)

def admin_required(fn):
    @wraps(fn)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin: abort(403)
        return fn(*args, **kwargs)
    return wrapper

@admin.get("/")
@admin_required
def dashboard():
    requests = RentalRequest.query.order_by(RentalRequest.created_at.desc()).all()
    return render_template("admin.html", requests=requests, products=Product.query.count(), pending=RentalRequest.query.filter_by(status="Pendiente").count())

@admin.route("/productos", methods=["GET","POST"])
@admin_required
def products():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        if not name:
            flash("El nombre es obligatorio.", "error")
        else:
            product = Product(name=name, description=request.form.get("description",""), price=request.form.get("price",0), stock=request.form.get("stock",0), image_url=request.form.get("image_url",""), category_id=request.form.get("category_id") or None)
            db.session.add(product); db.session.commit()
            flash("Producto agregado.", "success")
        return redirect(url_for("admin.products"))
    return render_template("admin_products.html", products=Product.query.order_by(Product.id.desc()).all(), categories=Category.query.all())

@admin.post("/productos/<int:product_id>/eliminar")
@admin_required
def delete_product(product_id):
    product = db.session.get(Product, product_id)
    if product:
        product.active = False
        db.session.commit()
    return redirect(url_for("admin.products"))

@admin.post("/solicitudes/<int:request_id>/estado")
@admin_required
def update_status(request_id):
    rental = db.session.get(RentalRequest, request_id)
    if not rental: abort(404)
    status = request.form.get("status")
    allowed = ["Pendiente","Aprobada","Rechazada","En preparación","Entregada","Devuelta","Finalizada","Cancelada"]
    if status in allowed:
        rental.status = status
        db.session.commit()
    return redirect(url_for("admin.dashboard"))
