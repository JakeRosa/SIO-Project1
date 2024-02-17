import session
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from models import Product, Review, User

unauthenticated = Blueprint(
    "unauthenticated",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

@unauthenticated.route("/products", methods=["GET"])
def products():
    local_session = session.SessionLocal()
    products = local_session.query(Product).all()
    local_session.close()
    return render_template("products.html", products=products)

@unauthenticated.route("/products/<id>", methods=["GET", "POST"])
def product(id):
    local_session = session.SessionLocal()

    if request.method == "POST":
        if current_user.is_anonymous:
            flash("Please login to leave a review.")
            return redirect(url_for("auth.login"))
        
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        
        comment = comment.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
        
        review = Review(user_id=current_user.id, product_id=id, rating=rating, comment=comment)

        local_session.add(review)
        local_session.commit()
        local_session.close()

        flash("Review added successfully.")
        return redirect(url_for("unauthenticated.product", id=id)) 
    else:
        product = local_session.query(Product).filter(Product.id == id).first()
        reviews = local_session.query(Review).filter(Review.product_id == id).join(User).all()
        return render_template("product.html", product=product, reviews=reviews)
    
    
