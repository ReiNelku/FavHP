from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required
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
            return render_template(
                "error.html", code="400", reason="must-provide-username"
            )
        # Check if email is submitted
        elif not email:
            return render_template(
                "error.html", code="400", reason="must-provide-email"
            )
        # Check if password is submitted
        elif not password:
            return render_template(
                "error.html", code="400", reason="must-provide-password"
            )
        # Check if password confirmation is submitted
        elif not confirmation:
            return render_template(
                "error.html", code="400", reason="must-type-your-password-again"
            )

        # Query database for user
        user = db.execute(
            "SELECT * FROM users WHERE username = ? AND email = ?", username, email
        )

        # Check if user already exists
        if len(user) != 0:
            return render_template(
                "error.html", code="400", reason="user-already-exists"
            )

        # Check if password and password confirmation match
        if not password == confirmation:
            return render_template(
                "error.html", code="400", reason="passwords-do-not-match"
            )

        # Create a new user in database
        user = db.execute(
            "INSERT INTO users (username, email, hash) VALUES(?, ?, ?)",
            username,
            email,
            generate_password_hash(password),
        )

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
            return render_template(
                "error.html", code="403", reason="must-provide-username-or-email"
            )
        # Check if password is submitted
        elif not password:
            return render_template(
                "error.html", code="403", reason="must-provide-password"
            )

        # Query database for user
        user = db.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?", namemail, namemail
        )

        # Ensure user exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return render_template(
                "error.html",
                code="403",
                reason="invalid-username,email-and~sor-password",
            )

        # Remember logged in user
        session["user_id"] = user[0]["id"]

        # Redirect user to homepage
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Logout the user
    session.clear()

    # Redirect user to homepage
    return redirect("/")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    # Change user password
    if request.method == "POST":
        current = request.form.get("current")
        new = request.form.get("new")
        confirmation = request.form.get("confirmation")

        # Check if current password is submitted
        if not current:
            return render_template(
                "error.html", code="400", reason="must-provide-current-password"
            )
        # Check if new password is submitted
        elif not new:
            return render_template(
                "error.html", code="400", reason="must-provide-new-password"
            )
        # Check if password confirmation is submitted
        elif not confirmation:
            return render_template(
                "error.html", code="400", reason="must-provide-password-confirmation"
            )

        # Get current user's password hash
        current_hash = db.execute(
            "SELECT hash FROM users WHERE id = ?", session["user_id"]
        )

        # Check if user has inputted correct password
        if not check_password_hash(current_hash[0]["hash"], current):
            return render_template("error.html", code="400", reason="invalid-password")

        # Check if new and old passwords are the same
        if current == new:
            return render_template(
                "error.html", code="400", reason="new-and-old-passwords-are-the-same"
            )

        # Check if new password and password confirmation match
        if not new == confirmation:
            return render_template(
                "error.html", code="400", reason="new-passwords-do-not-match"
            )

        # Generate hash for new password
        new_hash = generate_password_hash(new)

        # Update user password
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?", new_hash, session["user_id"]
        )

        # Log out user
        session.clear()

        return redirect("/")
    else:
        return render_template("password.html")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Query database for all headphone specifications
    headphones = db.execute(
        "SELECT headphones.id AS id, manufacturer.name AS manufacturer, headphones.model AS model, connectivity.type AS connectivity, form_factor.type AS form_factor, openness.type AS openness, driver.type AS driver, headphones.sensitivity AS sensitivity, sens_unit.unit AS sens_unit, headphones.impedance AS impedance, headphones.weight AS weight, headphones.image AS image FROM headphones INNER JOIN manufacturer ON headphones.manufacturer_id = manufacturer.id INNER JOIN connectivity ON headphones.connectivity_id = connectivity.id INNER JOIN form_factor ON headphones.form_factor_id = form_factor.id INNER JOIN openness ON headphones.openness_id = openness.id INNER JOIN driver ON headphones.driver_id = driver.id INNER JOIN sens_unit ON headphones.sens_unit_id = sens_unit.id"
    )
    # Query database for manufacturer list
    manufacturer_list = db.execute("SELECT * FROM manufacturer")

    if request.method == "POST":
        # Get user preference
        preference = request.form["vote"]

        # Update database with user preference
        db.execute(
            "UPDATE users SET preference_id = ? WHERE id = ?",
            preference,
            session["user_id"],
        )
        return redirect("/")
    else:
        return render_template(
            "index.html", headphones=headphones, manufacturer_list=manufacturer_list
        )


@app.route("/ranking")
@login_required
def ranking():
    # Query database for a headphone ranking by votes
    headphone_ranking = db.execute("SELECT COUNT(users.preference_id) AS votes, manufacturer.name AS manufacturer, headphones.model AS model FROM headphones INNER JOIN users ON headphones.id = users.preference_id INNER JOIN manufacturer ON headphones.manufacturer_id = manufacturer.id ORDER BY votes")

    return render_template("ranking.html", headphone_ranking=headphone_ranking)