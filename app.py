from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "prime-video-secret-key"

def create_database():
    connection = sqlite3.connect("users.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            movie_name TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    try:
        connection.execute(
            "ALTER TABLE watchlist ADD COLUMN poster_url TEXT"
        )
    except sqlite3.OperationalError:
        pass
    connection.commit()
    connection.close()


@app.route("/")
def home():
    connection = sqlite3.connect("users.db")
    connection.row_factory = sqlite3.Row

    if "user_id" in session:
        movies = connection.execute(
            "SELECT * FROM watchlist WHERE user_id = ?",
            (session["user_id"],)
        ).fetchall()
    else:
        movies = []

    connection.close()

    return render_template("index.html", movies=movies)

@app.route("/add_to_list", methods=["POST"])
def add_to_list():
    if "user_id" not in session:
        return redirect(url_for("login"))

    movie_name = request.form["movie_name"]
    poster_url = request.form["poster_url"]

    connection = sqlite3.connect("users.db")

    connection.execute(
        "INSERT INTO watchlist (user_id, movie_name, poster_url) VALUES (?, ?, ?)",
        (session["user_id"], movie_name, poster_url)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))

@app.route("/remove_from_list/<int:movie_id>")
def remove_from_list(movie_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = sqlite3.connect("users.db")

    connection.execute(
        "DELETE FROM watchlist WHERE id = ? AND user_id = ?",
        (movie_id, session["user_id"])
    )

    connection.commit()
    connection.close()

    return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("users.db")
        connection.row_factory = sqlite3.Row

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("home"))

        return render_template("login.html", error="Invalid email or password.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        connection = sqlite3.connect("users.db")

        connection.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )

        connection.commit()
        connection.close()

        return redirect(url_for("login"))

    return render_template("signup.html")


if __name__ == "__main__":
    create_database()
    app.run(debug=True)