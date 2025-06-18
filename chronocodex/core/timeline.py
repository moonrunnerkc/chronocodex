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

    if n_clusters < 1:
        print("Not enough data to form clusters.")
        return [], None

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
    timeline = sorted(timeline, key=lambda x: ids.index(x["id"]))

    if not timeline:
        print("Timeline is empty after processing.")  # Sanity check

    return timeline, kmeans

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
