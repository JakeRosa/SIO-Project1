import os
import re

import session
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_cors import CORS
from flask_login import current_user, login_required, login_user
from models import (Order, OrderItem, Product, Review, User, Wishlist,
                    WishlistProduct)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

authenticated = Blueprint(
    "authenticated",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

CORS(authenticated, resources={r"/*": {"origins": "https://127.0.0.1:5001"}})

@authenticated.route("/profile")
@login_required
def profile():
    return render_template(
        "profile.html", name=current_user.first_name + " " + current_user.last_name
    )

@authenticated.route("/profile/edit/<id>", methods=["GET", "POST"])
@login_required
def profile_edit(id):
    local_session = session.SessionLocal()

    if id != str(current_user.id):
        flash("You can only edit your own profile.")
        return redirect(url_for("authenticated.profile"))

    if request.method == "POST":
        # Get form information.
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        profile_picture = request.files.get("profile_picture")

        if profile_picture and not profile_picture.filename.endswith((".jpg", ".jpeg", ".png")):
            flash("Invalid file format.")
            return redirect(url_for("authenticated.profile_edit", id=id))
        
        # Check if user exists.
        user = local_session.query(User).filter(User.id == id).first()
        SpecialSym = "~`! @#$%^&*()_-+={[}]|\:;\"'<,>.?/"

        print(password)

        if password and check_password_hash(current_user.password, password):
            new_password = request.form.get("new_password")
            if new_password:
                confirm_new_password = request.form.get("confirm_password")
                if new_password != password and new_password == confirm_new_password:
                    if len(new_password) < 8:
                        flash("Password must have at least 8 characters.")
                        return redirect(url_for("authenticated.profile_edit", id=id))
                    elif not any(char.isdigit() for char in new_password):
                        flash("Password must contain at least 1 number")
                        return redirect(url_for("authenticated.profile_edit", id=id))
                    elif not any(char.isupper() for char in new_password):
                        flash("Password must contain at least 1 uppercase letter")
                        return redirect(url_for("authenticated.profile_edit", id=id))
                    elif not any(char.islower() for char in new_password):
                        flash("Password must contain at least 1 lowercase letter")
                        return redirect(url_for("authenticated.profile_edit", id=id))
                    elif not any(char in SpecialSym for char in new_password):
                        flash("Password must contain at least 1 special character")
                        return redirect(url_for("authenticated.profile_edit"), id=id)
                    else:
                        user.password = generate_password_hash(new_password)
                elif new_password == password:
                    flash("New password must be different from old password.")
                    return redirect(url_for("authenticated.profile_edit", id=id))
                else:
                    flash("New password and confirm new password don't match.")
                    return redirect(url_for("authenticated.profile_edit", id=id))
        else:
            flash("Wrong password.")
            return redirect(url_for("authenticated.profile_edit", id=id))

        # Update user information.
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                flash("Invalid email format. Please enter a valid email address.")
                return redirect(url_for("authenticated.profile_edit", id=id))
            user.email = email
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join("/app_sec/api/static/pictures", filename))
            user.profile_picture = filename

        # Commit changes.
        local_session.commit()

        # Redirect to profile page.
        flash("Profile updated successfully.")
        return redirect(url_for("authenticated.profile"))

    user = local_session.query(User).filter(User.id == id).first()
    return render_template("profile_edit.html", user=user)

@authenticated.route("/products/add_to_cart/<id>", methods=["POST"])
@login_required
def add_to_cart(id):
    local_session = session.SessionLocal()

    if current_user.is_anonymous:
        flash("Please login to add products to your cart.")
        return redirect(url_for("auth.login"))

    # Get form information.
    quantity = int(request.form.get("quantity"))


    user_order = local_session.query(Order).filter_by(user_id=current_user.id, is_finished=False).first()

    if user_order is None:
        user_order = Order(user_id=current_user.id)
        local_session.add(user_order)
        local_session.commit()

    order_item = local_session.query(OrderItem).filter_by(order_id=user_order.id, product_id=id).first()

    if order_item is None:
        order_item = OrderItem(order_id=user_order.id, product_id=id, quantity=quantity)
        local_session.add(order_item)
    else:
        order_item.quantity += quantity
    
    local_session.commit()
    local_session.close()

    flash("Product added to cart.")
    return redirect(url_for("unauthenticated.product", id=id))

@authenticated.route("/cart")
@login_required
def cart():
    local_session = session.SessionLocal()

    user_order = local_session.query(Order).filter_by(user_id=current_user.id, is_finished=False).first()

    if user_order is None:
        flash("Your cart is empty.")
        return render_template("cart.html", order_items=None)

    order_items = local_session.query(OrderItem).filter_by(order_id=user_order.id).all()


    # total = 0
    # for order_item in order_items:
    #     total += order_item.product.price * order_item.quantity

    total_price = sum([order_item.product.price * order_item.quantity for order_item in order_items])

    user_order.total_price = total_price

    local_session.commit()   

    return render_template("cart.html", order_items=order_items, total_price=total_price)

@authenticated.route("/cart/remove/<id>", methods=["POST"])
@login_required
def remove_from_cart(id):
    local_session = session.SessionLocal()

    user_order = local_session.query(Order).filter_by(user_id=current_user.id, is_finished=False).first()

    id_parts = id.split("-")

    if len(id_parts) != 2:
        flash("Invalid product id.")
        return redirect(url_for("authenticated.cart"))

    order_id, product_id = map(int, id_parts)

    order_item = local_session.query(OrderItem).filter_by(order_id=order_id, product_id=product_id).first()

    if not order_item:
        flash("Product not found.")
        return redirect(url_for("authenticated.cart"))

    product_name = order_item.product.name

    local_session.delete(order_item)
    local_session.commit()
    local_session.close()

    flash(f"{product_name} removed from cart.")
    return redirect(url_for("authenticated.cart"))

@authenticated.route('/change_stock/<int:product_id>', methods=['POST'])
def change_stock(product_id):
    local_session = session.SessionLocal()

    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403

    # Get the new stock quantity from the request data
    data = request.get_json()
    new_stock_quantity = data.get('new_stock_quantity')

    if new_stock_quantity is None:
        return jsonify({'message': 'New stock quantity not specified'}), 400

    # Retrieve the product from the database
    product = local_session.query(Product).filter_by(id=product_id).first()

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Update the stock quantity
    product.stock_quantity = new_stock_quantity

    if product.stock_quantity == "0":
        product.in_stock = False

    # Commit the changes to the database
    local_session.commit()

    return jsonify({'message': 'Stock quantity updated'})

@authenticated.route("/cart/checkout", methods=["POST"])
@login_required
def checkout():
    # Create a session
    local_session = session.SessionLocal()

    try:
        # Retrieve the current user's order
        user_order = local_session.query(Order).filter_by(user_id=current_user.id, is_finished=False).first()

        if user_order is None:
            return jsonify({'message': 'No active order found'}), 404

        # Loop through OrderItems
        for order_item in user_order.order_items:
            product = order_item.product

            # Deduct the ordered quantity from the product's stock
            if product.stock_quantity >= order_item.quantity:
                product.stock_quantity -= order_item.quantity
            else:
                return jsonify({'message': 'Insufficient stock for product: ' + product.name}), 400

        # Mark the order as finished and commit changes
        user_order.is_finished = True
        
        if product.stock_quantity == 0:
            product.in_stock = False
        
        local_session.commit()

        return jsonify({'message': 'Checkout successful'}), 200

    except Exception as e:
        local_session.rollback()
        return jsonify({'message': 'Error during checkout'}), 500

    finally:
        local_session.close()
        return redirect(url_for("unauthenticated.products"))

@authenticated.route("/orders")
@login_required
def orders():
    local_session = session.SessionLocal()

    orders = local_session.query(Order).filter_by(user_id=current_user.id, is_finished=True).join(OrderItem).all()

    return render_template("orders.html", orders=orders)

@authenticated.route("/cart/update/<id>", methods=["POST"])
@login_required
def update_cart(id):
    local_session = session.SessionLocal()

    user_order = local_session.query(Order).filter_by(user_id=current_user.id, is_finished=False).first()

    id_parts = id.split("-")

    if len(id_parts) != 2:
        flash("Invalid product id.")
        return redirect(url_for("authenticated.cart"))

    order_id, product_id = map(int, id_parts)

    order_item = local_session.query(OrderItem).filter_by(order_id=order_id, product_id=product_id).first()

    if not order_item:
        flash("Product not found.")
        return redirect(url_for("authenticated.cart"))

    quantity = int(request.form.get("quantity"))

    if quantity <= 0:
        flash("Invalid quantity.")
        return redirect(url_for("authenticated.cart"))

    order_item.quantity = quantity

    local_session.commit()
    local_session.close()

    flash("Cart updated.")
    return redirect(url_for("authenticated.cart"))

@authenticated.route("/products/add_to_wishlist/<id>", methods=["POST"])
@login_required
def add_to_wishlist(id):
    local_session = session.SessionLocal()

    if current_user.is_anonymous:
        flash("Please login to add products to your wishlist.")
        return redirect(url_for("auth.login"))

    user_wishlist = local_session.query(Wishlist).filter_by(user_id=current_user.id).first()

    if user_wishlist is None:
        user_wishlist = Wishlist(user_id=current_user.id)
        local_session.add(user_wishlist)
        local_session.commit()

    productu_wishlist = local_session.query(WishlistProduct).filter_by(wishlist_id=user_wishlist.id, product_id=id).first()

    if productu_wishlist is not None:
        flash("The product is already on your wishlist.")
    else:
        wishlist_product = WishlistProduct(wishlist_id=user_wishlist.id, product_id=id)
        local_session.add(wishlist_product)
        flash("Product added to your wishlist.")
    
    local_session.commit()
    local_session.close()
    return redirect(url_for("unauthenticated.product", id=id))

@authenticated.route("/wishlist")
@login_required
def wishlist():
    local_session = session.SessionLocal()

    user_wishlist = local_session.query(Wishlist).filter_by(user_id=current_user.id).first()

    if user_wishlist is None:
        flash("Your wishlist is empty.")
        return render_template("wishlist.html", wishlist_products=None)
    
    wishlist_products = local_session.query(WishlistProduct).filter_by(wishlist_id=user_wishlist.id).all()

    return render_template("wishlist.html", wishlist_products=wishlist_products)

@authenticated.route("/wishlist/remove/<id>", methods=["POST"])
@login_required
def remove_from_wishlist(id):
    local_session = session.SessionLocal()

    user_wishlist = local_session.query(Wishlist).filter_by(user_id=current_user.id).first()

    id_parts = id.split("-")

    if len(id_parts) != 2:
        flash("Invalid product id.")
        return redirect(url_for("authenticated.wishlist"))

    wishlist_id, product_id = map(int, id_parts)

    wishlist_product = local_session.query(WishlistProduct).filter_by(wishlist_id=wishlist_id, product_id=product_id).first()

    if not wishlist_product:
        flash("Product not found.")
        return redirect(url_for("authenticated.wishlist"))

    product_name = wishlist_product.product.name

    local_session.delete(wishlist_product)
    local_session.commit()
    local_session.close()

    flash(f"{product_name} removed from wishlist.")
    return redirect(url_for("authenticated.wishlist"))

@authenticated.route("/wishlist/empty", methods=["POST"])
@login_required
def empty_wishlist():
    local_session = session.SessionLocal()

    user_wishlist = local_session.query(Wishlist).filter_by(user_id=current_user.id).first()

    if user_wishlist is None:
        flash("Your wishlist is empty.")
        return redirect(url_for("authenticated.wishlist"))
    
    wishlist_products = local_session.query(WishlistProduct).filter_by(wishlist_id=user_wishlist.id).all()

    for wishlist_product in wishlist_products:
        local_session.delete(wishlist_product)
    
    local_session.commit()
    local_session.close()

    flash("Wishlist emptied.")
    return redirect(url_for("authenticated.wishlist"))