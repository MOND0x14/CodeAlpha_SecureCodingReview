from flask import Flask, request
import sqlite3
import subprocess
import os

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")


def get_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))

    result = cursor.fetchone()
    conn.close()

    return result


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    user = get_user(username, password)

    if user:
        return "Login successful"

    return "Invalid credentials", 401


@app.route("/ping")
def ping():
    host = request.args.get("host", "")

    result = subprocess.run(
        ["ping", "-c", "1", "--", host],
        capture_output=True,
        text=True,
        timeout=5
    )

    return result.stdout


if __name__ == "__main__":
    app.run(debug=False)
