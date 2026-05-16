# CineBot — AI Movie Recommendation Chatbot

CineBot is a multi-turn conversational movie recommender powered by the OpenAI API. Instead of returning a list from a single query, CineBot asks clarifying questions about your mood, genre preferences, and streaming platform before making a personalized recommendation with an explanation.

---

## Setup

**Requirements:** Python 3.11+

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

```bash
cp .env.example .env
```

Open `.env` and replace `your_openai_api_key_here` with your actual OpenAI API key.

---

## Run the app

```bash
python app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

---

## Run the evaluation

```bash
python eval/eval.py
```

This runs 10 labeled test cases and prints accuracy to the terminal. Results are saved to `eval/results.json`.

---

## Project structure

```
├── app.py               # Flask backend + system prompt
├── requirements.txt     # Pinned dependencies
├── .env.example         # API key template
├── static/
│   └── index.html       # Frontend chat UI
├── eval/
│   ├── eval.py          # Evaluation harness + 10 test cases
│   └── results.json     # Generated after running eval
└── REPORT.md            # Project writeup
```

---

## Environment variables

| Variable        | Description              |
|-----------------|--------------------------|
| `OPENAI_API_KEY`| Your OpenAI API key      |
