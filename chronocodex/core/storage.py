# storage.py
<<<<<<< HEAD
=======
# Author: Bradley R Kinnard
# License: MIT
# Description: SQLite-based storage backend for Chronocodex
# Supports commit metadata storage, vector serialization, and structured querying
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)

import sqlite3
import os
import json

<<<<<<< HEAD
# Database file path
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "chronocodex.db"))

# Initialize the SQLite database schema
=======
# Database file path for Chronocodex
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "chronocodex.db"))

# Initialize the SQLite database schema with commit metadata and vector blob
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS commits (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            author TEXT,
            summary TEXT,
<<<<<<< HEAD
            embedding TEXT
=======
            vector BLOB,
            date TEXT
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)
        )
    ''')
    conn.commit()
    conn.close()

<<<<<<< HEAD
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
=======
# Store a commit with its metadata and embedding vector into the database
def store_commit_vector(commit_id, timestamp, author, summary, vector, date=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO commits (id, timestamp, author, summary, vector, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (commit_id, timestamp, author, summary, json.dumps(vector), date))
    conn.commit()
    conn.close()

# Alias for compatibility with CLI module
store_commit = store_commit_vector

# Retrieve all embeddings (used for clustering or semantic search vector ops)
def get_all_embeddings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, summary, vector FROM commits')
    rows = c.fetchall()
    conn.close()
    return [(row[0], row[1], json.loads(row[2])) for row in rows]

# Retrieve full commit metadata including vector and timestamp (used in UI + summarizer)
def load_commit_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, author, timestamp, summary, vector, date FROM commits')
    rows = c.fetchall()
    conn.close()

    data = []
    for row in rows:
        commit_id, author, timestamp, summary, vector_blob, date = row
        try:
            vector = json.loads(vector_blob)
        except Exception:
            continue
        data.append({
            "commit": commit_id,
            "author": author,
            "timestamp": timestamp,
            "summary": summary,
            "vector": vector,
            "date": date
        })
    return data
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)
