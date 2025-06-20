<<<<<<< HEAD
import gradio as gr
from chronocodex.core.timeline import generate_timeline, get_similar_summaries
from chronocodex.core.embedder import embed_text
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Load timeline once for display
def load_timeline():
    timeline, _ = generate_timeline()
    return "\n\n".join([
        f"[Cluster {e['cluster']}] {e['id']}: {e['summary']}"
        for e in timeline
    ])

# Handle semantic search
def query_summary(user_query):
=======
#!/usr/bin/env python3
# app.py — Chronocodex UI Entry Point
# Author: Bradley R Kinnard
# License: MIT

import gradio as gr
import sys
import os

# Include Chronocodex core path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Core imports
from chronocodex.core.timeline import generate_timeline, get_similar_summaries
from chronocodex.core.embedder import embed_text


# --- Load Timeline View with Cluster and Date Info ---
def load_timeline():
    """
    Generate timeline with cluster and commit summaries.
    Includes commit date when available.
    """
    timeline, _ = generate_timeline()
    return "\n\n".join([
        f"[Cluster {e['cluster']}] {e['id']} (Date: {e.get('date', 'unknown')}): {e['summary']}"
        for e in timeline
    ])


# --- Semantic Search Based on User Prompt ---
def query_summary(user_query):
    """
    Embed the user query and return top matching commit summaries
    with similarity score and date metadata.
    """
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)
    try:
        vector = embed_text(user_query)
        results = get_similar_summaries(vector)
        return "\n\n".join([
<<<<<<< HEAD
            f"{r['id']} (score={r['similarity']:.2f}): {r['summary']}"
=======
            f"{r['id']} (Date: {r.get('date', 'unknown')}, Score: {r['similarity']:.2f}): {r['summary']}"
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)
            for r in results
        ])
    except Exception as e:
        return f"Error: {str(e)}"

<<<<<<< HEAD
with gr.Blocks(title="Chronocodex UI") as demo:
    gr.Markdown("# Chronocodex: Semantic Commit Explorer")
=======

# --- Gradio UI ---
with gr.Blocks(title="Chronocodex UI") as demo:
    gr.Markdown("# Chronocodex: Semantic Commit Explorer")
    gr.Markdown("Built by Bradley R Kinnard — MIT Licensed")
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)

    with gr.Tab("🗂 Timeline View"):
        timeline_box = gr.Textbox(label="Timeline (Clustered)", lines=25)
        timeline_btn = gr.Button("Refresh Timeline")
        timeline_btn.click(load_timeline, outputs=timeline_box)

    with gr.Tab("🔍 Semantic Query"):
        query_input = gr.Textbox(label="Describe a change you're looking for")
        query_btn = gr.Button("Search Commits")
        query_output = gr.Textbox(label="Matching Commits", lines=10)
        query_btn.click(query_summary, inputs=query_input, outputs=query_output)

<<<<<<< HEAD
=======
# --- App Launch ---
>>>>>>> 4a78c9d6 (Refactored for open-source release: portable pathing, CLI-ready, no hardcoded repo)
demo.launch()
