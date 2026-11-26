from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product, Category, RentalRequest, RentalItem

main = Blueprint("main", __name__)

@main.get("/")
def index():
    products = Product.query.filter_by(active=True).order_by(Product.id.desc()).limit(4).all()
    return render_template("index.html", products=products)

@main.get("/catalogo")
def catalog():
    category_id = request.args.get("categoria", type=int)
    search = request.args.get("q","").strip()
    query = Product.query.filter_by(active=True)
    if category_id: query = query.filter_by(category_id=category_id)
    if search: query = query.filter(Product.name.ilike(f"%{search}%"))
    return render_template("catalog.html", products=query.order_by(Product.name).all(), categories=Category.query.order_by(Category.name).all(), selected=category_id, search=search)

@main.route("/solicitar", methods=["GET", "POST"])
@login_required
def request_rental():
    if request.method == "POST":
        try:
            delivery = date.fromisoformat(request.form["delivery_date"])
            returned = date.fromisoformat(request.form["return_date"])
        except (ValueError, KeyError):
            flash("Ingresá fechas válidas.", "error")
            return redirect(url_for("main.request_rental"))
        address = request.form.get("address","").strip()
        ids = request.form.getlist("product_id")
        quantities = request.form.getlist("quantity")
        if not address or delivery < date.today() or returned < delivery or not ids:
            flash("Revisá dirección, fechas y productos seleccionados.", "error")
            return redirect(url_for("main.catalog"))
        rental = RentalRequest(user_id=current_user.id, delivery_date=delivery, return_date=returned, address=address, notes=request.form.get("notes","").strip())
        db.session.add(rental)
        db.session.flush()
        for pid, qty in zip(ids, quantities):
            product = db.session.get(Product, int(pid))
            amount = int(qty)
            if product and product.active and amount > 0:
                db.session.add(RentalItem(request_id=rental.id, product_id=product.id, quantity=amount, unit_price=product.price))
        if not rental.items:
            db.session.rollback()
            flash("Seleccioná al menos un producto.", "error")
            return redirect(url_for("main.catalog"))
        db.session.commit()
        flash(f"Solicitud #{rental.id} enviada. Quedó pendiente de confirmación.", "success")
        return redirect(url_for("main.my_requests"))
    return render_template("request.html", products=Product.query.filter_by(active=True).all())

@main.get("/mis-solicitudes")
@login_required
def my_requests():
    requests = RentalRequest.query.filter_by(user_id=current_user.id).order_by(RentalRequest.created_at.desc()).all()
    return render_template("my_requests.html", requests=requests)
