from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from collections import Counter



app = Flask(__name__)
app.config["DEBUG"] = True
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="kpashko",
    password="mydatabase",
    hostname="kpashko.mysql.pythonanywhere-services.com",
    databasename="kpashko$notes",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Note(db.Model):

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    unique = db.Column(db.Integer)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html")

    article=request.form["contents"]
    counter = len(Counter(article.split()))
    note = Note(content=article, unique = counter)
    db.session.add(note)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/notes")
def notes():
    return render_template("notes.html", notes=Note.query.order_by((Note.unique).desc()))
