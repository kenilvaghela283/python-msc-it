from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# Database connection
def get_db():
    conn = sqlite3.connect("todo.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create table
def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# READ
@app.route("/")
def home():
    conn = get_db()

    tasks = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


# CREATE
@app.route("/add", methods=["POST"])
def add():
    task = request.form["task"]

    conn = get_db()

    conn.execute(
        "INSERT INTO tasks (task) VALUES (?)",
        (task,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# UPDATE
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    task = request.form["task"]

    conn = get_db()

    conn.execute(
        "UPDATE tasks SET task = ? WHERE id = ?",
        (task, id)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)