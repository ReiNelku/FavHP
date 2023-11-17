from flask import Flask, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        ...
    else:
        return render_template("register.html")