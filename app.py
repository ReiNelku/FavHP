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
        
        # Query database for user
        user = db.execute("SELECT * FROM users WHERE username = ? AND email = ?", username, email)

        # Check if user already exists
        if len(user) != 0:
            return render_template("error.html", code="400", reason="user-already-exists")

        # Check if password and password confirmation match
        if not password == confirmation:
            return render_template("error.html", code="400", reason="passwords-do-not-match")
    else:
        return render_template("register.html")