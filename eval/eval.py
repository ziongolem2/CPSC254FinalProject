"""
eval.py — Evaluation harness for CineBot movie recommender.

Metric:
  accuracy = (# responses where the recommended movie matches the user's stated
              genre + mood constraints AND includes title + genre + reasoning +
              streaming platform) / (# test inputs)

Usage:
  python eval/eval.py
"""

import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
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

# ── Test cases ──────────────────────────────────────────────────────────────
# Each test case is a multi-turn conversation ending in a recommendation.
# "expected" contains the constraints the final recommendation must satisfy.
TEST_CASES = [
    {
        "id": "tc01",
        "conversation": [
            {"role": "user",      "content": "I want to watch something funny tonight."},
            {"role": "assistant", "content": "Fun! Are you in the mood for a comedy with a lot of heart, or something more absurd and silly? And do you have a preferred streaming platform?"},
            {"role": "user",      "content": "Absurd and silly. I have Netflix."},
        ],
        "expected": {
            "genre": "comedy",
            "platform": "netflix",
            "mood": "absurd or silly"
        }
    },
    {
        "id": "tc02",
        "conversation": [
            {"role": "user",      "content": "I'm in the mood for something scary."},
            {"role": "assistant", "content": "Nice! Do you prefer psychological horror or more traditional jump-scare style? And how much time do you have?"},
            {"role": "user",      "content": "Psychological horror, about 2 hours. I use Hulu."},
        ],
        "expected": {
            "genre": "horror",
            "platform": "hulu",
            "mood": "psychological"
        }
    },
    {
        "id": "tc03",
        "conversation": [
            {"role": "user",      "content": "I want a classic movie."},
            {"role": "assistant", "content": "Love it! Are you thinking a classic drama, romance, or something more like an old adventure film? Any streaming platform preference?"},
            {"role": "user",      "content": "Classic romance. I have HBO Max."},
        ],
        "expected": {
            "genre": "romance",
            "platform": "hbo max",
            "mood": "classic"
        }
    },
    {
        "id": "tc04",
        "conversation": [
            {"role": "user",      "content": "Show me something underrated."},
            {"role": "assistant", "content": "Happy to dig into some hidden gems! What kind of mood are you in — action, drama, sci-fi, something else? And what platforms do you have?"},
            {"role": "user",      "content": "Sci-fi, something thought-provoking. I have Prime Video."},
        ],
        "expected": {
            "genre": "sci-fi",
            "platform": "prime video",
            "mood": "underrated or thought-provoking"
        }
    },
    {
        "id": "tc05",
        "conversation": [
            {"role": "user",      "content": "I need a good action movie."},
            {"role": "assistant", "content": "Awesome! Do you want something fast-paced and explosive, or more of a thriller with action elements? What platform are you on?"},
            {"role": "user",      "content": "Fast-paced and explosive. Netflix."},
        ],
        "expected": {
            "genre": "action",
            "platform": "netflix",
            "mood": "fast-paced"
        }
    },
    {
        "id": "tc06",
        "conversation": [
            {"role": "user",      "content": "I want to watch a documentary."},
            {"role": "assistant", "content": "Great choice! Are you interested in a nature documentary, something true crime, or maybe a social or political one? Any platform preference?"},
            {"role": "user",      "content": "True crime. I have Netflix."},
        ],
        "expected": {
            "genre": "documentary",
            "platform": "netflix",
            "mood": "true crime"
        }
    },
    {
        "id": "tc07",
        "conversation": [
            {"role": "user",      "content": "Something for a date night."},
            {"role": "assistant", "content": "How romantic! Do you want something heartwarming and sweet, or maybe a fun comedy you can laugh at together? And what streaming service do you have?"},
            {"role": "user",      "content": "Heartwarming and sweet. Disney+."},
        ],
        "expected": {
            "genre": "romance or drama",
            "platform": "disney+",
            "mood": "heartwarming"
        }
    },
    {
        "id": "tc08",
        "conversation": [
            {"role": "user",      "content": "I want to watch something with my kids."},
            {"role": "assistant", "content": "Family movie night! How old are the kids? And are you looking for something animated or live action? Any platform you're on?"},
            {"role": "user",      "content": "They're 8 and 10. Animated is fine. We have Disney+."},
        ],
        "expected": {
            "genre": "animation or family",
            "platform": "disney+",
            "mood": "family-friendly"
        }
    },
    {
        "id": "tc09",
        "conversation": [
            {"role": "user",      "content": "I'm feeling sad and want to cry."},
            {"role": "assistant", "content": "Sometimes a good cry is exactly what you need! Do you want a tearjerker drama, or maybe something bittersweet with a hopeful ending? What platform are you on?"},
            {"role": "user",      "content": "A real tearjerker. I use Hulu."},
        ],
        "expected": {
            "genre": "drama",
            "platform": "hulu",
            "mood": "emotional or tearjerker"
        }
    },
    {
        "id": "tc10",
        "conversation": [
            {"role": "user",      "content": "I want something based on a true story."},
            {"role": "assistant", "content": "Love those! Are you in the mood for an inspiring story, a crime/thriller based on real events, or something more historical? What platform do you have?"},
            {"role": "user",      "content": "Inspiring. I have Netflix."},
        ],
        "expected": {
            "genre": "drama or biography",
            "platform": "netflix",
            "mood": "inspiring"
        }
    },
    {
        "id": "tc11",
        "conversation": [
            {"role": "user",      "content": "I want a thriller."},
            {"role": "assistant", "content": "Nice! Do you prefer something psychological or more action-driven? And what platform are you on?"},
            {"role": "user",      "content": "Psychological. I have Netflix."},
            {"role": "assistant", "content": "I'd recommend **Gone Girl** — it's a gripping psychological thriller full of twists, perfect for your mood. It's available on Netflix."},
            {"role": "user",      "content": "I've already seen that one, can you suggest something else?"},
        ],
        "expected": {
            "genre": "thriller",
            "platform": "netflix",
            "mood": "psychological"
        }
    },
    {
        "id": "tc12",
        "conversation": [
            {"role": "user",      "content": "I want a sci-fi movie."},
            {"role": "assistant", "content": "Fun! Are you in the mood for something action-packed or more thought-provoking? What platform do you have?"},
            {"role": "user",      "content": "Action-packed. I have Prime Video."},
            {"role": "assistant", "content": "I'd recommend **Edge of Tomorrow** — a fast-paced sci-fi action film with great replay value. It's available on Prime Video."},
            {"role": "user",      "content": "That sounds too intense, I want something a bit lighter and more fun."},
        ],
        "expected": {
            "genre": "sci-fi",
            "platform": "prime video",
            "mood": "light or fun"
        }
    },
    {

        "id": "tc13",
        "conversation": [
            {"role": "user",      "content": "Recommend me a movie."},
            {"role": "assistant", "content": "I'd love to help! What kind of mood are you in — comedy, drama, thriller, something else? And what streaming platform do you have?"},
            {"role": "user",      "content": "I'm in the mood for a thriller. I have Netflix."},
        ],
        "expected": {
            "genre": "thriller",
            "platform": "netflix",
            "mood": "suspenseful"
        }
    },
    {

        "id": "tc14",
        "conversation": [
            {"role": "user",      "content": "I want something emotional and inspiring."},
            {"role": "assistant", "content": "That sounds wonderful! Are you in the mood for a drama, a true story, or something else? And what streaming platform do you have?"},
            {"role": "user",      "content": "Maybe a drama, and I only have Netflix."},
        ],
        "expected": {
            "genre": "drama",
            "platform": "netflix",
            "mood": "emotional and inspiring"
        }
    },
    {

        "id": "tc15",
        "conversation": [
            {"role": "user",      "content": "I want a sci-fi movie."},
            {"role": "assistant", "content": "Cool! Do you want something fast-paced or more mind-bending? And what platform are you on?"},
            {"role": "user",      "content": "Something fast-paced on Hulu."},
            {"role": "assistant", "content": "I'd recommend **Interstellar** — it's a visually stunning and fast-moving sci-fi epic available on Hulu."},
            {"role": "user",      "content": "I've already seen that."},
            {"role": "assistant", "content": "No problem! Are you okay with something more recent, or would you like an older classic? Any sub-genre you prefer — space, dystopian, time travel?"},
            {"role": "user",      "content": "Something more recent with a time travel element on Hulu."},
        ],
        "expected": {
            "genre": "sci-fi",
            "platform": "hulu",
            "mood": "fast-paced or time travel"
        }
    },
    {

        "id": "tc16",
        "conversation": [
            {"role": "user",      "content": "I'm in the mood for a funny movie."},
            {"role": "assistant", "content": "Nice! Do you prefer lighthearted and silly, or something with a darker edge? And what platform are you on?"},
            {"role": "user",      "content": "I like dark comedies and I have Prime Video."},
            {"role": "assistant", "content": "I'd recommend **In Bruges** — it's a wickedly funny dark comedy with sharp writing and great performances. Available on Prime Video."},
            {"role": "user",      "content": "Can you suggest another one?"},
        ],
        "expected": {
            "genre": "comedy",
            "platform": "prime video",
            "mood": "dark or funny"
        }
    },
    {

        "id": "tc17",
        "conversation": [
            {"role": "user",      "content": "I need a movie for tonight."},
            {"role": "assistant", "content": "Sure! How much time do you have, and what kind of mood are you in?"},
            {"role": "user",      "content": "I only have about 90 minutes and want something suspenseful."},
            {"role": "assistant", "content": "Great, a tight suspenseful film it is! What streaming platform do you have?"},
            {"role": "user",      "content": "I have Netflix."},
        ],
        "expected": {
            "genre": "thriller or suspense",
            "platform": "netflix",
            "mood": "suspenseful"
        }
    },
    {

        "id": "tc18",
        "conversation": [
            {"role": "user",      "content": "I want something family-friendly but still interesting for adults."},
            {"role": "assistant", "content": "Great combo! Are you open to animated films, or do you prefer live action? And what platform are you on?"},
            {"role": "user",      "content": "Animated is fine, and we have Disney+."},
        ],
        "expected": {
            "genre": "animation or family",
            "platform": "disney+",
            "mood": "family-friendly"
        }
    },
    {

        "id": "tc19",
        "conversation": [
            {"role": "user",      "content": "I don't know what I want to watch."},
            {"role": "assistant", "content": "That's okay, let's figure it out! How are you feeling right now — do you want something light and fun, or more serious and emotional? And what platform are you on?"},
            {"role": "user",      "content": "Something light and fun. I have Netflix."},
        ],
        "expected": {
            "genre": "comedy or animation",
            "platform": "netflix",
            "mood": "light or fun"
        }
    },
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def get_recommendation(conversation: list[dict]) -> str:
    """Send a completed conversation to the model and get its recommendation."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.0,   # deterministic for eval
        max_tokens=600,
    )
    return response.choices[0].message.content


def score_response(reply: str, expected: dict) -> tuple[bool, dict]:
    """
    Score a single recommendation response.
    Returns (passed: bool, details: dict)

    Checks:
      1. Contains a movie title (heuristic: quoted or bolded word)
      2. Mentions the expected genre (or a synonym)
      3. Mentions the expected streaming platform
      4. Contains a reasoning/why explanation (heuristic: sentence count >= 2)

    If any expected field is missing (e.g. no genre/platform defined),
    that check is marked False and the test case fails gracefully.
    """
    reply_lower = reply.lower()

    # CHECK 1: Does the reply contain a movie title?
    # We look for text wrapped in **bold**, or a quoted "Title"
    has_title = False
    if "**" in reply:
        has_title = True
    elif '"' in reply:
        has_title = True

    # CHECK 2: Does the reply mention the expected genre?
    # expected["genre"] can be "romance or drama", so we split on " or " and check each word
    # If genre is not defined in expected, has_genre stays False and the test fails gracefully
    has_genre = False
    for keyword in expected.get("genre", "").lower().split(" or "):
        if keyword.strip() and keyword.strip() in reply_lower:
            has_genre = True

    # CHECK 3: Does the reply mention the expected streaming platform?
    # Same logic as genre — split on " or " in case there are multiple acceptable platforms
    # If platform is not defined in expected, has_platform stays False and the test fails gracefully
    has_platform = False
    for keyword in expected.get("platform", "").lower().split(" or "):
        if keyword.strip() and keyword.strip() in reply_lower:
            has_platform = True

    # CHECK 4: Does the reply contain actual reasoning (not just a one-liner)?
    # We split the reply into sentences and count ones that are long enough to be meaningful
    has_reasoning = False
    sentences = []
    for sentence in reply.split("."):
        sentence = sentence.strip()
        if len(sentence) > 20:
            sentences.append(sentence)
    if len(sentences) >= 2:
        has_reasoning = True

    # The response only passes if ALL four checks are satisfied
    passed = has_title and has_genre and has_platform and has_reasoning

    details = {
        "has_title":     has_title,
        "has_genre":     has_genre,
        "has_platform":  has_platform,
        "has_reasoning": has_reasoning,
    }
    return passed, details


# ── Main ─────────────────────────────────────────────────────────────────────

def run_eval():
    results = []
    passed_count = 0

    print(f"\n{'='*60}")
    print(f"  CineBot Evaluation — {len(TEST_CASES)} test cases")
    print(f"{'='*60}\n")

    for tc in TEST_CASES:
        print(f"Running {tc['id']}...", end=" ", flush=True)
        try:
            reply = get_recommendation(tc["conversation"])
            passed, details = score_response(reply, tc["expected"])
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({"id": tc["id"], "passed": False, "error": str(e)})
            continue

        if passed:
            passed_count += 1
            print("✅ PASS")
        else:
            print("❌ FAIL")
            failing = [k for k, v in details.items() if not v]
            print(f"   Failed checks: {', '.join(failing)}")
            print(f"   Reply snippet: {reply[:120]}...")

        results.append({
            "id":      tc["id"],
            "passed":  passed,
            "details": details,
            "reply":   reply
        })

    accuracy = passed_count / len(TEST_CASES)
    print(f"\n{'='*60}")
    print(f"  Accuracy: {passed_count}/{len(TEST_CASES)} = {accuracy:.1%}")
    print(f"{'='*60}\n")

    # Save results
    out_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(out_path, "w") as f:
        json.dump({"accuracy": accuracy, "results": results}, f, indent=2)
    print(f"Full results saved to {out_path}")


if __name__ == "__main__":
    run_eval()