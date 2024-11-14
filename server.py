from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products.html")
def products():
    return render_template("products.html")

@app.route("/favorites.html")
def favorites():
    return render_template("favorites.html")

@app.route("/signin.html")
def signin():
    return render_template("signin.html")

@app.route("/signup.html")
def signup():
    return render_template("signup.html")

@app.route("/account.html")
def account():
    return render_template("account.html")

if __name__ == "__main__":
    app.run("127.0.0.1", port=80)
