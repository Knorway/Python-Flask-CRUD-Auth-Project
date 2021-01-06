import os
from flask import Flask, render_template, request, redirect
from models import db, FastUser
from flask_wtf import CSRFProtect
from forms import RegisterForm

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        fast_user = FastUser()
        fast_user.userid = form.data.get("userid")
        fast_user.username = form.data.get("username")
        fast_user.password = form.data.get("password")

        db.session.add(fast_user)
        db.session.commit()

        return redirect("/")

    return render_template("register.html", form=form)


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, "db.sqlite")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbfile
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "SECRET_KET_12345"

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()

    app.run(host="127.0.0.1", port=5000, debug=True)
