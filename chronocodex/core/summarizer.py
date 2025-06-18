#!/usr/bin/env python3
"""
summarizer.py — Git Diff Summarization Module for Chronocodex

Author: Bradley Ryan Kinnard
License: MIT

Description:
This module supports code diff summarization using both OpenAI's direct API
and LangChain's LLM abstraction layer. It enables 1–2 sentence summaries
to describe the purpose and effect of Git commit diffs.

Environment:
Requires an .env file or environment variable: OPENAI_API_KEY

Dependencies:
- openai>=1.0.0
- langchain
- python-dotenv
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

# Load environment variables from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- OpenAI direct API summarization using v1 client ---
def summarize_diff_openai(diff_text):
    """
    Use OpenAI's direct API (v1 client) to summarize a git diff.
    """
    if not diff_text.strip():
        return "No meaningful code change."
    try:
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": "You are a code review assistant."},
            {"role": "user", "content": f"Summarize the following git diff in 1‑2 sentences:\n{diff_text}"}
        ]
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI API error: {e}"


# --- LangChain-based summarization ---
try:
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain

    def init_llm():
        """
        Initialize LangChain's ChatOpenAI wrapper with environment API key.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set.")
        return ChatOpenAI(temperature=0.3, model="gpt-4", openai_api_key=api_key)

    # Prompt template for LangChain summarization
    template = """
    Analyze this code diff:
    {diff}

    What functionality changed and why? Output a 1-2 sentence summary.
    """
    prompt = PromptTemplate.from_template(template)
    chain = LLMChain(llm=init_llm(), prompt=prompt)

    def summarize_diff(diff_text):
        """
        Main summarization function using LangChain.
        """
        if not diff_text or not diff_text.strip():
            return "No meaningful code change."
        try:
            summary = chain.run(diff=diff_text.strip())
            return summary.strip()
        except Exception as e:
            return f"LangChain error: {e}"

except ImportError:
    summarize_diff = summarize_diff_openai


# --- Optional test block ---
if __name__ == "__main__":
    test_diff = "@@ -1,2 +1,3 @@\ndef foo():\n    print('Hello world')\n+def bar(): return 42"
    print("LangChain Summary:", summarize_diff(test_diff))
    print("OpenAI API Summary:", summarize_diff_openai(test_diff))
