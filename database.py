import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "career.db"
CAREERS_JSON = BASE_DIR / "data" / "careers.json"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS careers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT NOT NULL,
        skills TEXT NOT NULL,
        courses TEXT NOT NULL,
        jobs TEXT NOT NULL,
        roadmap TEXT NOT NULL,
        salary_range TEXT NOT NULL,
        demand_level TEXT NOT NULL,
        education TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        related_interests TEXT NOT NULL,
        project_ideas TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS assessment_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        option_e TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        payload TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    seed_careers(conn)
    seed_questions(conn)
    conn.commit()
    conn.close()


def seed_careers(conn):
    data = json.loads(CAREERS_JSON.read_text(encoding="utf-8"))
    for career in data:
        conn.execute("""
            INSERT OR REPLACE INTO careers
            (name, description, skills, courses, jobs, roadmap, salary_range,
             demand_level, education, difficulty, related_interests, project_ideas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            career["name"],
            career["description"],
            json.dumps(career["skills"]),
            json.dumps(career["courses"]),
            json.dumps(career["jobs"]),
            json.dumps(career["roadmap"]),
            career["salary_range"],
            career["demand_level"],
            career["education"],
            career["difficulty"],
            json.dumps(career["related_interests"]),
            json.dumps(career["project_ideas"])
        ))


def seed_questions(conn):
    questions = [
        ("When given a difficult problem, what do you prefer?",
         "Analyze data", "Build a technical solution", "Design a creative solution",
         "Research the problem", "Organize a team/business solution"),
        ("Which activity sounds most interesting?",
         "Finding patterns in datasets", "Writing code or building software", "Creating an interface",
         "Investigating how systems work", "Planning a product or business"),
        ("What type of challenge motivates you?",
         "Mathematical/analytical puzzles", "Complex technical bugs", "Visual/creative problems",
         "Security or investigation problems", "People/process problems"),
        ("Which work environment sounds best?",
         "Data-focused", "Engineering-focused", "Creative studio",
         "Security/research lab", "Business/team environment"),
        ("What would you most like to build?",
         "A prediction dashboard", "A useful application", "A polished digital experience",
         "A secure system", "A product used by many people"),
        ("Which subject area would you explore further?",
         "Statistics and mathematics", "Computer science", "Design and human behavior",
         "Networks and security", "Business and economics"),
        ("When learning something new, you prefer to:",
         "Experiment with data", "Code a small project", "Sketch and prototype",
         "Read technical documentation", "Discuss use cases and strategy"),
        ("Which outcome feels most satisfying?",
         "Discovering an insight", "Making a system work", "Making something intuitive",
         "Finding and fixing a vulnerability", "Improving a process"),
        ("How do you usually approach ambiguity?",
         "Look for evidence and patterns", "Break it into technical tasks",
         "Explore several creative concepts", "Research risks and constraints",
         "Clarify goals and stakeholders"),
        ("Which project would you pick for a weekend?",
         "Build a data/ML model", "Build a web or mobile app", "Design a prototype",
         "Set up a security lab", "Plan a product and user journey")
    ]
    conn.execute("DELETE FROM assessment_questions")
    conn.executemany("""
        INSERT INTO assessment_questions
        (question, option_a, option_b, option_c, option_d, option_e)
        VALUES (?, ?, ?, ?, ?, ?)
    """, questions)


def get_careers():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM careers ORDER BY name").fetchall()
    conn.close()
    return [deserialize_career(dict(row)) for row in rows]


def get_career_by_name(name):
    conn = get_connection()
    row = conn.execute("SELECT * FROM careers WHERE name = ?", (name,)).fetchone()
    conn.close()
    return deserialize_career(dict(row)) if row else None


def get_questions():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM assessment_questions ORDER BY id").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_result(student_name, payload):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO results (student_name, payload) VALUES (?, ?)",
        (student_name, json.dumps(payload))
    )
    conn.commit()
    result_id = cur.lastrowid
    conn.close()
    return result_id


def deserialize_career(career):
    for field in ("skills", "courses", "jobs", "roadmap", "related_interests", "project_ideas"):
        career[field] = json.loads(career[field])
    return career
