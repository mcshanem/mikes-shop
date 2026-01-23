from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from dotenv import load_dotenv
import os
from flask_login import LoginManager, login_required, logout_user, login_user
from forms import LoginForm, RegisterForm, AddToCartForm
from db import db, User, Item
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

# Load variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI")

# Connect Bootstrap to Flask app
Bootstrap5(app)

# Connect SQLAlchemy to Flask app and generate database
db.init_app(app)
with app.app_context():
    db.create_all()

# Create login manager and connect it to Flask app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shop")
@login_required
def shop():
    print("In shop view")
    form = AddToCartForm()
    items = db.session.scalars(db.select(Item)).all()
    return render_template("shop.html", items=items, form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    print("In login view")
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if user is None:
            flash("Invalid email, please try again.", "error")
        elif not check_password_hash(user.password, form.password.data):
            flash("Invalid password, please try again.", "error")
        else:
            login_user(user)
            return redirect(url_for("shop"))
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.data)
        new_user = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            name=form.name.data,
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration Successful")
        except IntegrityError:
            flash(
                "That email is already associated with an account. Log in instead.",
                "error",
            )

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
