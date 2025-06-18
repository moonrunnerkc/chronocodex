# storage.py

import sqlite3
import os
import json

# Database file path
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "chronocodex.db"))

# Initialize the SQLite database schema
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS commits (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            author TEXT,
            summary TEXT,
            embedding TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Store a commit with its metadata and embedding vector
def store_commit_vector(commit_id, timestamp, author, summary, vector):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO commits (id, timestamp, author, summary, embedding)
        VALUES (?, ?, ?, ?, ?)
    ''', (commit_id, timestamp, author, summary, json.dumps(vector)))
    conn.commit()
    conn.close()

# Alias for compatibility with CLI import
store_commit = store_commit_vector

# Retrieve all embeddings from the database
def get_all_embeddings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, summary, embedding FROM commits')
    rows = c.fetchall()
    conn.close()
    return [(row[0], row[1], json.loads(row[2])) for row in rows]
