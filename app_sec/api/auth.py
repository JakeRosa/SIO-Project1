import session
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user
from models import User
from werkzeug.security import check_password_hash, generate_password_hash
import re

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form information.
        email = request.form.get("email")
        password = request.form.get("password")

        local_session = session.SessionLocal()

        user = local_session.query(User).filter(User.email == email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("auth.test"))

    return render_template("login.html")


@auth.route("/test")
@login_required
def test():
    return render_template(
        "test.html", name=current_user.first_name + " " + current_user.last_name
    )

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")

        local_session = session.SessionLocal()

        user = local_session.query(User).filter(User.email == email).first()
        SpecialSym = "~`! @#$%^&*()_-+={[}]|\:;\"'<,>.?/"

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format. Please enter a valid email address.")
            return redirect(url_for("auth.register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters")
            return redirect(url_for("auth.register"))
        elif not any(char.isdigit() for char in password):
            flash("Password must contain at least 1 number")
            return redirect(url_for("auth.register"))
        elif not any(char.isupper() for char in password):
            flash("Password must contain at least 1 uppercase letter")
            return redirect(url_for("auth.register"))
        elif not any(char.islower() for char in password):
            flash("Password must contain at least 1 lowercase letter")
            return redirect(url_for("auth.register"))
        elif not any(char in SpecialSym for char in password):
            flash("Password must contain at least 1 special character")
            return redirect(url_for("auth.register"))

        if not user:
            user = User(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
            flash("Account successfully created!")
            return redirect(url_for("auth.login"))

        flash("Email already exists!")
        return redirect(url_for("auth.register"))
    return render_template("register.html")
