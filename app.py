from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from sqlite3 import connect, IntegrityError
from functools import wraps
from random import randint
import bcrypt

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db_conn = connect("GreenPrint.db", check_same_thread=False)
db_cursor = db_conn.cursor()


@app.route("/")
def index():
    get_session = session.get("user_id")
    return render_template("index.html", get_session=get_session)


# Reutilizamos login_required de pset9 (en si, eso esta dentro de los docs de flask jajaja) para validar accesos a rutas
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def validate_user_loged(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect("/userconsole")
        return f(*args, **kwargs)

    return decorated_function


@app.route("/singup", methods=["POST", "GET"])
@validate_user_loged
def singup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        get_password = request.form["password"]

        bytes = get_password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes, salt)

        try:
            db_cursor.execute(
                "INSERT INTO users (username, mail, password) VALUES (?, ?, ?)",
                (username, email, hashed_password),
            )
            db_conn.commit()
            return redirect("/login")
        except IntegrityError:
            try:
                db_cursor.execute(
                    "SELECT username FROM users WHERE username = ?", (username,)
                )
                validate_repeated_name = db_cursor.fetchone()[0]
            except TypeError:
                validate_repeated_name = None
            try:
                db_cursor.execute("SELECT mail FROM users WHERE mail = ?", (email,))
                validate_repeated_mail = db_cursor.fetchone()[0]
            except TypeError:
                validate_repeated_mail = None

            if validate_repeated_name == username:
                flash("El nombre ingresado ya esta registrado", "error")
            if validate_repeated_mail == email:
                flash("El correo ingresado ya esta registrado", "error")

            return redirect("/singup")

    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
@validate_user_loged
def login():
    if request.method == "POST":
        form_username = request.form["username"]
        form_password = request.form["password"]

        db_cursor.execute("SELECT * FROM users WHERE username = ?", (form_username,))
        query_data = db_cursor.fetchall()

        if len(query_data) != 0:
            validate_password = query_data[0][3]

            form_password_bytes = form_password.encode("utf-8")

            if bcrypt.checkpw(form_password_bytes, validate_password):
                session["user_id"] = query_data[0][0]
                session["user"] = query_data[0][1]
                session["mail"] = query_data[0][2]
                return redirect("/")
            else:
                return redirect("/singup")
        else:
            return redirect("/singup")
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/buy")
@login_required
def buy():
    get_session = session.get("user_id")
    user_name = session.get("user")
    mail = session.get("mail")
    return render_template(
        "buy.html", get_session=get_session, user_name=user_name, mail=mail
    )


@app.route("/buy_transaction", methods=["POST", "GET"])
@login_required
def buy_transaction():
    if request.method == "POST":
        card = request.form["cardNumber"]
        exp = request.form["expiryDate"]
        cvv = request.form["cvv"]
        amount = request.form["quantity"]

        for i in range(0, int(amount)):
            generate_machine_id = randint(1, 100000)
            db_cursor.execute(
                "SELECT CARD_ID from card_info WHERE card_num = ?", (card,)
            )
            card_id = db_cursor.fetchall()

            if len(card_id) == 0:
                db_cursor.execute(
                    "INSERT INTO card_info (card_num, cvv, expiry_date) VALUES (?, ?, ?)",
                    (card, exp, cvv),
                )
                db_conn.commit()

                db_cursor.execute(
                    "SELECT CARD_ID from card_info WHERE card_num = ?", (card,)
                )
                card_id = db_cursor.fetchall()

            db_cursor.execute(
                "INSERT INTO buys (user_id, card_id, machine_id) VALUES (?, ?, ?)",
                (session.get("user_id"), card_id[0][0], generate_machine_id),
            )
            db_cursor.execute(
                "INSERT INTO machine_register (user_id, machine_id) VALUES (?, ?)",
                (session.get("user_id"), generate_machine_id),
            )
            db_conn.commit()

        return redirect("/")

    else:
        return redirect("/buy")


@app.route("/userconsole")
@login_required
def console():
    username = session.get("user")

    db_cursor.execute(
        "SELECT MACHINE_ID FROM machine_register WHERE user_id = ?",
        (session.get("user_id"),),
    )
    machine_id = db_cursor.fetchall()

    if len(machine_id) != 0:
        return render_template("console.html", username=username, machine_id=machine_id)
    else:
        return render_template("console.html", username=username, machine_id=None)


@app.route("/team")
def team():
    get_session = session.get("user_id")
    return render_template("team.html", get_session=get_session)


@app.route("/portfolio")
def portfolio():
    get_session = session.get("user_id")
    return render_template("portfolio.html", get_session=get_session)


@app.route("/contact")
def contact():
    get_session = session.get("user_id")
    return render_template("contact.html", get_session=get_session)


if __name__ == "__main__":
    try:
        # Start the Flask app
        app.run(debug=False, host="127.0.0.1", port=5000)
    finally:
        db_cursor.close()
        db_conn.close()
