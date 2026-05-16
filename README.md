# CineBot — AI Movie Recommendation Chatbot

CineBot is a multi-turn conversational movie recommender powered by the OpenAI API. Instead of returning a list from a single query, CineBot asks clarifying questions about your mood, genre preferences, and streaming platform before making a personalized recommendation with an explanation.

---

## Setup

**Requirements:** Python 3.11+

> **Note:** On Mac/Linux use `python3` and `pip3`. On Windows use `py` and `pip`.

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Create and activate a virtual environment

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```bash
py -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

**Mac/Linux:**
```bash
pip3 install -r requirements.txt
```

**Windows:**
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

**Mac/Linux:**
```bash
python3 app.py
```

**Windows:**
```bash
py app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

---

## Run the evaluation

**Mac/Linux:**
```bash
python3 eval/eval.py
```

**Windows:**
```bash
py eval/eval.py
```

This runs 19 labeled test cases and prints accuracy to the terminal. Results are saved to `eval/results.json`.

---

## Project structure

```
├── app.py               # Flask backend + system prompt
├── requirements.txt     # Pinned dependencies
├── .env.example         # API key template
├── static/
│   └── index.html       # Frontend chat UI
├── eval/
│   └── eval.py          # Evaluation harness + 19 test cases
└── REPORT.md            # Project writeup
```

---

## Environment variables

| Variable        | Description              |
|-----------------|--------------------------|
| `OPENAI_API_KEY`| Your OpenAI API key      |
