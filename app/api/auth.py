import session
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from models import User

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
        if not email or not password:
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))
        # Check if user exists.
        local_session = session.SessionLocal()

        result = local_session.execute("SELECT * FROM users WHERE email = '" + email + "' AND password = '" + password + "'").fetchall()


        if result:
            user = local_session.query(User).filter(User.email == email).first()
            login_user(user)
            return redirect(url_for("index"))

        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))


        # if len(user) != 1 :
        #     flash("Please check your login details and try again.")
        #     return redirect(url_for("auth.login")) 

        #user = local_session.query(User).filter(User.email == email).first()

        #local_session.close()
        # if not user or not (user.password == password):
        #     flash("Please check your login details and try again.")
        #     return redirect(url_for("auth.login"))

        # login_user(user)
        # return redirect(url_for("auth.test"))

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")

        user = session.engine.execute("SELECT * FROM users WHERE email = '" + email + "'").fetchall()

        if not user:
            session.engine.execute("INSERT INTO users (first_name, last_name, email, password) VALUES ('" + first_name + "', '" + last_name + "', '" + email + "', '" + password + "')")
            flash("Account successfully created!")
            return redirect(url_for("auth.login"))
        flash("Email already exists!")
        return redirect(url_for("auth.register"))
    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))