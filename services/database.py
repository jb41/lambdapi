import sqlite3



database_name = "functions.db"


def create_table():
    with sqlite3.connect(database_name) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS functions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                slug TEXT,
                runtime TEXT,
                code TEXT,
                created_at DATETIME NOT NULL,
                UNIQUE (slug)
            );
        """)

        db.execute("""
            CREATE INDEX functions_slug_index ON functions (slug);
        """)

        db.commit()


def seed_database():
    with sqlite3.connect(database_name) as db:
        with open('seed.sql', 'r') as f:
            seed_script = f.read()

        db.executescript(seed_script)
        db.commit()
