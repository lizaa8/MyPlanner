
import sqlite3
from pathlib import Path
from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="MyPlanner API")

DB_PATH = Path(__file__).with_name("myplanner.db")


# Define what an assignment looks like
class Assignment(BaseModel):
    name: str
    course: str
    due_date: date


# Create database if it doesn't exist
def setup_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                course TEXT,
                due_date TEXT,
                completed INTEGER DEFAULT 0
            )
        """)


setup_database()


# Home endpoint
@app.get("/")
def home():
    return {"message": "MyPlanner API is running!"}


# Retrieve saved assignments
@app.get("/assignments")
def get_assignments():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM assignments ORDER BY due_date"
        ).fetchall()

    return [dict(row) for row in rows]


# Save a new assignment
@app.post("/assignments")
def add_assignment(assignment: Assignment):
    if not assignment.name.strip():
        raise HTTPException(400, "Assignment name is required")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO assignments
            (name, course, due_date)
            VALUES (?, ?, ?)
            """,
            (
                assignment.name,
                assignment.course,
                assignment.due_date.isoformat()
            )
        )
        assignment_id = cursor.lastrowid

    return {
        "message": "Assignment saved!",
        "id": assignment_id
    }