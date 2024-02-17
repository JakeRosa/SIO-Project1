import auth
import authenticated
import init_db
import models
import session
import unauthenticated
from flask import Flask, render_template
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static",
)

# configuração do CORS
CORS(app, resources={r"/*": {"origins": "https://127.0.0.1:5001"}})


init_db.init_db()

app.secret_key = "123456"

app.jinja_env.autoescape = False
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

app.register_blueprint(auth.auth)
app.register_blueprint(authenticated.authenticated)
app.register_blueprint(unauthenticated.unauthenticated)


@app.route("/")
def index():
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    local_session = session.SessionLocal()
    user = local_session.query(models.User).filter(models.User.id == user_id).first()
    local_session.close()
    return user
