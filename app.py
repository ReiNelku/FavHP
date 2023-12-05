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
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if username is submitted
        if not username:
            return render_template("error.html", code="400", reason="must-provide-username")
        # Check if email is submitted    
        elif not email:
            return render_template("error.html", code="400", reason="must-provide-email")
        # Check if password is submitted    
        elif not password:
            return render_template("error.html", code="400", reason="must-provide-password")
        # Check if password confirmation is submitted
        elif not confirmation:
            return render_template("error.html", code="400", reason="must-type-your-password-again")
        
    else:
        return render_template("register.html")