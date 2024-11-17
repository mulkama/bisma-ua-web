import functools
import hashlib
from datetime import datetime, timedelta
from urllib import parse
import json
import re

import jwt
from flask import Flask, redirect, render_template, request, session, url_for

from database.models import User, db

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bisma.db"
app.secret_key = "Qdknewfkjcefkwejf&^&*%EDfwefwejfhwekjdI*&^*&%432yuet23ued23d))(U(FUEFUe9erfewfreferfe))"

db.init_app(app)

with app.app_context():
    db.create_all()


def generate_token(id, email):
    user_data = {"id": id, "email": email}
    token = jwt.encode(
        {"user": user_data, "exp": datetime.utcnow() + timedelta(days=365)}, app.config["SECRET_KEY"], algorithm="HS256"
    )
    return token


def require_login(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        if "logged_in" in session:
            user = User.query.filter_by(id=session["user_id"]).first()
            return f(user, *args, **kwargs)
        else:
            redirect_to = parse.urlsplit(request.url).path
            return redirect(url_for("login") + f"?url={redirect_to}")

    return inner


def require_token(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        token = re.findall(r"Bearer (.+)", request.headers.get("Authorization", ""))
        if token:
            token = token[0]
        else:
            token = request.args.get("token")

        if not token:
            return {"_code": False, "_msg": "Missing Bearer token"}, 401

        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            user = User.query.filter_by(id=payload["user"]["id"]).first()
        except jwt.ExpiredSignatureError as e:
            return {"_code": False, "_msg": "Token has expired"}, 401
        except jwt.InvalidTokenError as e:
            return {"_code": False, "_msg": "Invalid token"}, 401
        except Exception as e:
            return {"_code": False, "_msg": e}, 400

        if not user:
            return {"_code": False, "_msg": "Missing such user"}, 400

        return f(user=user, *args, **kwargs)

    return inner


@app.route("/")
def index(*args, **kwargs):
    return render_template("index.html")


@app.route("/products/")
@require_login
def products(*args, **kwargs):
    return render_template("products.html")


@app.route("/favorites/")
@require_login
def favorites(*args, **kwargs):
    return render_template("favorites.html")


@app.route("/account/")
@require_login
def account(*args, **kwargs):
    return render_template("account.html")


@app.route("/login/", methods=["GET", "POST"])
def login(*args, **kwargs):
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        hash = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter_by(email=email, password=hash).first()
        if user:
            session["logged_in"] = True
            session["user_email"] = user.email
            session["user_id"] = user.id
            redirect_to = request.args.get("url", "/")
            response = redirect(redirect_to)
            token = generate_token(user.id, user.email)
            response.set_cookie("token", token)
            return response
        else:
            error = "Invalid Credentials. Please try again."

    return render_template("login.html", error=error)


@app.route("/signup/", methods=["GET", "POST"])
def signup(*args, **kwargs):
    error = None
    if request.method == "POST":
        username = request.form["email"]
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if not user:
            hash = hashlib.sha256(password.encode()).hexdigest()
            user = User(
                username=username,
                email=email,
                password=hash,
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            error = "User already exists."

    return render_template("signup.html", error=error)


@app.route("/api/products/", methods=["GET", "POST", "DELETE"])
@require_token
def api_products(user: User, *args, **kwargs):
    return json.loads(open("products.json", encoding="utf-8").read())


@app.route("/api/favorites/", methods=["GET", "POST", "DELETE"])
@require_token
def api_favorites(user: User, *args, **kwargs):
    if request.method == "GET":
        user = User.query.filter_by(email=user.email).first()
        return {"id": user.id, "username": user.username, "email": user.email}
    elif request.method == "POST":
        return 403
    elif request.method == "UPDATE":
        user.username = request.json["username"]
        db.session.add(user)
        db.session.commit()
        return 200
    elif request.method == "DELETE":
        if "logged_in" in session and session["logged_in"] == user.id:
            session.pop("logged_in")
            session.pop("user_id")
            session.pop("user_email")
        db.session.delete(user)
        db.session.commit()
        return 200
    # fetch("http://localhost:8087/api/")
    #   .then(response => response.json())
    #   .then(json => console.log(json))


if __name__ == "__main__":
    app.run("127.0.0.1", port=8080)
