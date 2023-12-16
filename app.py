from cs50 import SQL
from flask import abort, Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
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

        # Create a new user in database
        user = db.execute("INSERT INTO users (username, email, hash) VALUES(?, ?, ?)", username, email, generate_password_hash(password))
        
        # Log in with the newly created user
        session["user_id"] = id

        # Redirect user to homepage
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    namemail = request.form.get("namemail")
    password = request.form.get("password")

    if request.method == "POST":
        # Check if username or email is submitted
        if not namemail:
            return render_template("error.html", code="403", reason="must-provide-username-or-email")
        # Check if password is submitted
        elif not password:
            return render_template("error.html", code="403", reason="must-provide-password")
        
        # Query database for user
        user = db.execute("SELECT * FROM users WHERE username = ? OR email = ?", namemail, namemail)

        # Ensure user exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return render_template("error.html", code="403", reason="invalid-username,email-and~sor-password")

        # Remember logged in user
        session["user_id"] = user[0]["id"]

        # Redirect user to homepage
        return redirect("/")
    else:
        return render_template("login.html")