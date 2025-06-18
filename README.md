# 🕰 Chronocodex

Chronocodex is an open-source developer tool that integrates with Git repositories to generate a **semantic changelog** of code evolution. It summarizes developer intent for each commit, embeds those summaries as vectors, and offers both a **timeline UI** and **natural language query interface**.

---

### 🎥 Chronocodex Demo

<video controls width="100%">
  <source src="chronocodex/docs/demo/chronocodex.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

## 🎯 Features

- 📘 AI-generated semantic commit summaries
- 🔍 Natural language commit querying
- 🧠 Embedding-based vector search
- 📈 Timeline clustering by code topic
- 🖥 Gradio-based interactive interface
- 💻 CLI integration for scripting & automation

---

## 🔩 Architecture Overview

```text
                     ┌─────────────────────────────┐
                     │       Git Repository        │
                     └─────────────────────────────┘
                               │
                               ▼
                     ┌────────────────────────────┐
                     │      Diff Extraction        │
                     │         (GitPython)         │
                     └────────────────────────────┘
                               │
                               ▼
                     ┌────────────────────────────┐
                     │     Intent Summarizer      │
                     │   (OpenAI / LangChain)     │
                     └────────────────────────────┘
                               │
                               ▼
                     ┌────────────────────────────┐
                     │     Vector Embeddings       │
                     │    (OpenAI / FAISS/Chroma)  │
                     └────────────────────────────┘
                               │
                               ▼
                     ┌────────────────────────────┐
                     │     SQLite / Vector DB      │
                     └────────────────────────────┘
                               │
                               ▼
                ┌────────────────────────────────────────┐
                │           CLI / Gradio UI              │
                └────────────────────────────────────────┘
🛠 CLI Usage

chronocodex init
Initializes the local Chronocodex database.


chronocodex scan --repo /path/to/repo
Processes a Git repo, summarizing diffs and embedding them as vectors.


chronocodex query "When was authentication added?"
Perform a semantic search across commit history.

🧪 Sample Output

$ chronocodex scan --repo data/examples/sample_repo
[~] Found 4 commits
[+] Stored commit b30f076: The change in the code modifies the function `beta()` to return...
[+] Stored commit d8db82a: The code change adds a new function named 'beta'...
[✓] Scan complete.

$ chronocodex query "What functions were added recently?"
- f3be5a3 (score=0.81): A new function named 'bar' was added...
- d8db82a (score=0.79): The code change adds a new function named 'beta'...
📚 Core Modules
Module	Purpose
core/diff_parser.py	Git diff extraction via GitPython
core/summarizer.py	Summarizes code diffs using LLMs
core/embedder.py	Converts summaries into vector embeddings
core/storage.py	Stores commits, summaries, and vectors
core/timeline.py	Timeline generation and vector querying
cli/chronocodex_cli.py	CLI interface
ui/app.py	Interactive Gradio UI
tests/test_diff_parser.py	Commit diff parser tests

📦 Installation

git clone https://github.com/moonrunnerkc/chronocodex.git
cd chronocodex
pip install -r requirements.txt
Create a .env file with your OpenAI API key:

env
OPENAI_API_KEY=sk-...

👤 Author
Bradley Ryan Kinnard
Open-source builder, software engineer, and AI tooling architect.
📧 bradkinnard@proton.me
🔗 github.com/moonrunnerkc

⚖️ License
This project is released under the MIT License.
See LICENSE for full terms.

🌍 Open Source Mission
Chronocodex aims to bring semantic intelligence and searchability to version control — improving team collaboration, code reviews, and historical analysis.
We welcome forks, contributions, and research collaborations.

Built by developers, for developers — with transparency, intent, and history at the core.

📺 GitHub Pages / Demo Setup
Enable GitHub Pages from the docs/ folder in repository settings

Place demo video (chronocodex.mp4) in docs/demo/

Link is auto-embedded in this README above

