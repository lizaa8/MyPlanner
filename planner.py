
import sqlite3
from pathlib import Path

# Store the database next to this Python file
DB_PATH = Path(__file__).with_name("myplanner.db")


def setup_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                course TEXT,
                due_date TEXT,
                completed INTEGER DEFAULT 0
            )
        """)


def save_assignment(name, course, due_date):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO assignments (name, course, due_date)
            VALUES (?, ?, ?)
            """,
            (name, course, due_date)
        )

    print("Assignment saved!")


def show_assignments():
    with sqlite3.connect(DB_PATH) as connection:
        assignments = connection.execute(
            "SELECT name, course, due_date FROM assignments"
        ).fetchall()

    if not assignments:
        print("No assignments saved yet.")

    for name, course, due_date in assignments:
        print(f"{name} | {course} | Due: {due_date}")


setup_database()

# Add one example assignment (only on the first run)
with sqlite3.connect(DB_PATH) as connection:
    count = connection.execute(
        "SELECT COUNT(*) FROM assignments"
    ).fetchone()[0]

if count == 0:
    save_assignment(
        "Database Homework",
        "Computer Science",
        "2026-11-13"
    )

print("\nMYPLANNER - SAVED ASSIGNMENTS")
show_assignments()