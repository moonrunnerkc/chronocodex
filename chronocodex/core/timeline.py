<<<<<<< HEAD
import os
import numpy as np
from chronocodex.core.storage import get_all_embeddings
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

def generate_timeline(n_clusters=4):
    # Load commit embeddings from SQLite DB
    commits = get_all_embeddings()
    print(f"Loaded {len(commits)} commits from DB")
    
    if not commits:
        raise ValueError("No commits found in DB.")
        
    n_commits = len(commits)
    n_clusters = min(n_clusters, n_commits)  # prevent overshooting
=======
# timeline.py — Commit Timeline and Semantic Search
# Author: Bradley R Kinnard
# License: MIT

import os
import numpy as np
import sqlite3
import ast
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from chronocodex.core.storage import get_all_embeddings
from chronocodex.core.embedder import compute_similarity
from chronocodex.core.pipeline import DB_PATH


def generate_timeline(n_clusters=4):
    """
    Load commit embeddings, perform KMeans clustering, and generate a timeline view.
    Clusters commits and optionally includes commit metadata if available.
    """
    commits = get_all_embeddings()
    print(f"Loaded {len(commits)} commits from DB")

    if not commits:
        raise ValueError("No commits found in DB.")

    n_commits = len(commits)
    n_clusters = min(n_clusters, n_commits)  # Avoid requesting more clusters than points
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)

    if n_clusters < 1:
        print("Not enough data to form clusters.")
        return [], None

<<<<<<< HEAD
    # Unpack commit data
    ids, summaries, vectors = zip(*commits)
    X = np.array(vectors)

    # Run clustering to segment commits into topic clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(X)

    timeline = []

    # Assign cluster labels to each commit
    for i, label in enumerate(labels):
        print(f"Commit {ids[i]} => Cluster {label} | Summary: {summaries[i]}")  # Debug output
        timeline.append({
            "id": ids[i],
            "summary": summaries[i],
            "cluster": int(label)
        })

    # Sort timeline by original commit order
=======
    # Unpack commit data for clustering
    ids, summaries, vectors = zip(*commits)
    X = np.array(vectors)

    # Perform clustering on embedding vectors
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    labels = kmeans.fit_predict(X)

    # Reconnect to DB to fetch dates
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, date FROM commits")
    date_rows = dict(cursor.fetchall())
    conn.close()

    timeline = []

    # Merge cluster label and date into commit metadata
    for i, label in enumerate(labels):
        date = date_rows.get(ids[i], "unknown")  # Handle missing dates
        print(f"Commit {ids[i]} => Cluster {label} | Summary: {summaries[i]}")
        timeline.append({
            "id": ids[i],
            "summary": summaries[i],
            "cluster": int(label),
            "date": date  # ✅ include date for display and queries
        })

    # Preserve original commit order
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)
    timeline = sorted(timeline, key=lambda x: ids.index(x["id"]))

    if not timeline:
        print("Timeline is empty after processing.")  # Sanity check

    return timeline, kmeans

<<<<<<< HEAD
def get_similar_summaries(query_vector, top_k=5):
    # Load all embeddings and compute cosine similarity with query vector
    commits = get_all_embeddings()
    ids, summaries, vectors = zip(*commits)

    similarities = cosine_similarity([query_vector], vectors)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]

    return [
        {"id": ids[i], "summary": summaries[i], "similarity": float(similarities[i])}
        for i in top_indices
    ]

# Manual test/debug runner
if __name__ == "__main__":
    timeline, _ = generate_timeline()
    for entry in timeline:
        print(f"[Cluster {entry['cluster']}] {entry['id']}: {entry['summary']}")
=======

def get_similar_summaries(query_vector, top_k=5):
    """
    Given a query vector, return the top_k most similar commit summaries,
    including ID, summary text, similarity score, and commit date.
    """
    results = []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, summary, vector, date FROM commits")
    rows = cursor.fetchall()
    conn.close()

    parsed = []
    for commit_id, summary, vector_blob, commit_date in rows:
        if not vector_blob:
            continue
        try:
            if isinstance(vector_blob, (bytes, bytearray)):
                blob_str = vector_blob.decode('utf-8')
                vector = ast.literal_eval(blob_str)
            elif isinstance(vector_blob, str):
                vector = ast.literal_eval(vector_blob)
            else:
                raise ValueError("Unsupported vector type")

        except Exception as e:
            print(f"[ERROR] Failed to parse vector for commit {commit_id}: {e}")
            continue

        parsed.append((commit_id, summary, vector, commit_date))

    # Compute cosine similarity between query and each stored vector
    for commit_id, summary, vector, commit_date in parsed:
        sim = cosine_similarity([query_vector], [vector])[0][0]
        print(f"[SIM] Commit {commit_id} | Score: {sim:.4f} | Summary: {summary}")
        results.append({
            "id": commit_id,
            "summary": summary,
            "similarity": sim,
            "date": commit_date  # ✅ include date in similarity result
        })

    # Return top-k most similar results sorted by similarity
    results.sort(key=lambda r: r["similarity"], reverse=True)
    print(f"[DEBUG] Returning {len(results)} matches")

    return results[:top_k]


# Manual test/debug entry point
if __name__ == "__main__":
    timeline, _ = generate_timeline()
    for entry in timeline:
        print(f"[Cluster {entry['cluster']}] {entry['id']}: {entry['summary']} (Date: {entry['date']})")
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)
