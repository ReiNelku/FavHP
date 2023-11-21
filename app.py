from cs50 import SQL
from flask import abort, Flask, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite databse
db = SQL("sqlite:///favhp.db")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ...
    else:
        return render_template("register.html")