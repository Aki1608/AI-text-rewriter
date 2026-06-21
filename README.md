# AI Text Sculptor (LLM Rewriting Engine)

A high-performance Generative AI tool that intelligently rewrites text based on highly specific constraints. Built with **LangChain**, powered by **Groq's Llama-3**, and featuring a custom **Gradio** interface, this tool allows users to manipulate the tone, length, target audience, and language style of any given text.

A standout feature of this project is the **Visual Diff Engine**, which mathematically compares the original and generated text to highlight exact insertions and deletions in real-time, functioning similarly to a Git version control interface.

---

## Core Features

* **Lightning-Fast Inference:** Utilizes the Groq API (`llama-3.1-8b-instant`) to generate human-quality text rewrites in milliseconds.
* **Dynamic Prompt Engineering:** Dynamically constructs strict LLM system prompts based on UI dropdown selections (Tone, Length, Audience, Style).
* **Git-Style Visual Diffs:** Employs Python's native `difflib` to compute word-by-word state changes, mapping them to Gradio's `HighlightedText` component for a clear before/after analysis.

---

## Project Structure

* `rewriter_core.py`: The backend engine. Handles environment variables, LLM initialization, LangChain prompt templating, and the string-comparison diff logic.
* `app.py`: The frontend UI. A lightweight Gradio script that builds the dashboard and routes user inputs to the backend engine.
* `requirements.txt`: The project dependencies.

---

## Prerequisites

**1. Python Version:** This project requires **Python 3.10** or newer.

**2. Groq API Key:**
You will need a free API key from Groq to power the text generation.

---

## Installation & Setup

**1. Clone the repository:**

    git clone https://github.com/yourusername/AI-text-rewriter.git
    cd AI-text-rewriter

**2. Create and activate a virtual environment:**

* **Windows (PowerShell):**

    python -m venv venv
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
    .\venv\Scripts\activate

* **Linux / macOS / GitHub Codespaces:**

    python -m venv venv
    source venv/bin/activate

**3. Install dependencies:**

    pip install --upgrade pip
    pip install -r requirements.txt

**4. Set up Environment Variables:**
Create a `.env` file in the root directory and add your Groq API key:

    GROQ_API_KEY=your_groq_api_key_here

---

## Running the Application

Ensure your virtual environment is active, then launch the Gradio server:

    python app.py

Once the server starts, open the provided local URL (typically http://127.0.0.1:7860) in your web browser. 

Paste your source text into the left column, adjust the dials for your desired output, and click **Rewrite Text** to see the LLM at work.