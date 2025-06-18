import gradio as gr
from core.timeline import generate_timeline, get_similar_summaries
from core.embedder import embed_text
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
    try:
        vector = embed_text(user_query)
        results = get_similar_summaries(vector)
        return "\n\n".join([
            f"{r['id']} (score={r['similarity']:.2f}): {r['summary']}"
            for r in results
        ])
    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks(title="Chronocodex UI") as demo:
    gr.Markdown("# Chronocodex: Semantic Commit Explorer")

    with gr.Tab("🗂 Timeline View"):
        timeline_box = gr.Textbox(label="Timeline (Clustered)", lines=25)
        timeline_btn = gr.Button("Refresh Timeline")
        timeline_btn.click(load_timeline, outputs=timeline_box)

    with gr.Tab("🔍 Semantic Query"):
        query_input = gr.Textbox(label="Describe a change you're looking for")
        query_btn = gr.Button("Search Commits")
        query_output = gr.Textbox(label="Matching Commits", lines=10)
        query_btn.click(query_summary, inputs=query_input, outputs=query_output)

demo.launch()
