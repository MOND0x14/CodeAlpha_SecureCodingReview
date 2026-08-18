from flask import Flask, request
import sqlite3
import subprocess

app = Flask(__name__)

SECRET_KEY = "CodeAlphaSecret123"

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return """
    <h1>CodeAlpha Secure Coding Review</h1>
    <p>Test application for security code review.</p>
    <form action="/login" method="POST">
        <input name="username" placeholder="Username">
        <input name="password" placeholder="Password" type="password">
        <button type="submit">Login</button>
    </form>
    """

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db()

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    user = conn.execute(query).fetchone()

    if user:
        return f"Welcome {username}!"
    else:
        return "Invalid username or password"

@app.route("/ping")
def ping():
    host = request.args.get("host")

    result = subprocess.check_output(
        f"ping -c 1 {host}",
        shell=True
    )

    return result.decode()

if __name__ == "__main__":
    app.run(debug=True)
