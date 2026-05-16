from flask import Flask, request, jsonify, session, send_from_directory
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(24)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are CineBot, a warm and knowledgeable movie recommendation assistant. 
You engage in natural multi-turn conversation to learn what the user wants before making a recommendation.

RULES YOU MUST FOLLOW:
1. Before making any movie recommendation, you MUST ask at least one clarifying follow-up question 
   about the user's mood, preferred genre, available time, or streaming platform (Netflix, Hulu, etc.).
   Do not recommend a movie on the very first message — gather information first.

2. When you do make a recommendation, your response MUST include ALL of the following:
   - Movie title (bolded)
   - Genre
   - A personalized explanation of why you're recommending it based on what the user told you
   - The streaming platform(s) where it's available (e.g., Netflix, Hulu, Prime Video, Disney+)

3. Keep your tone friendly and conversational — like a knowledgeable friend, not a search engine.

4. If the user doesn't like a suggestion or wants something different, ask a follow-up question 
   to refine the recommendation rather than immediately listing more movies.

5. As soon as you have enough information to make a relevant recommendation
   (genre/mood and streaming platform), immediately provide a recommendation and
   avoid asking unnecessary additional follow-up questions. Even if the user provides
   super simple short sentences, this may still count as enough relevant information
   for you to make a movie recommendation, given that the user provides you with the
   genre/mood and streaming platform.
"""

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    history = data.get("history", [])

    if not user_message:
        return jsonify({"error": "No message provided."}), 400

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.8,
            max_tokens=600,
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/reset", methods=["POST"])
def reset():
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(debug=True)