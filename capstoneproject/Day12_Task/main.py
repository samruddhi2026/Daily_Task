import os
import requests
from Day11_Task.retriever import retrieve
from Day12_Task.router import IntentRouter
from Day12_Task.prompts import PROMPTS


def load_env(env_path):
    if not os.path.exists(env_path):
        return

    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value:
                os.environ.setdefault(key, value)


load_env(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env')))


def safety_check(query):
    banned = ["hate", "offensive", "abuse", "illegal"]

    if any(word in query.lower() for word in banned):
        return False

    if len(query.strip()) < 3:
        return False

    return True


def gemini_generate(prompt, model="text-bison-001"):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta2/models/{model}:generateText?key={api_key}"
    body = {
        "prompt": {"text": prompt},
        "temperature": 0.7,
        "maxOutputTokens": 300,
    }

    try:
        response = requests.post(url, json=body, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get("candidates", [{}])[0].get("output", "").strip()
    except Exception:
        return None


def generate_response(query):
    if not safety_check(query):
        return "Sorry, I cannot respond to that request."

    router = IntentRouter()
    intent = router.route(query)
    prompt = PROMPTS.get(intent, PROMPTS["general"])

    if intent == "recommendation":
        results = retrieve(query)

        if not results:
            return "No matching outfits found."

        output = "\nRecommended Outfit:\n\n"
        for i, item in enumerate(results, 1):
            output += f"{i}. {item['text'].title()}\n"
            output += f"   → Style: {item['style_vibe']}\n\n"

        gemini_text = gemini_generate(output)
        if gemini_text:
            return gemini_text

        return output

    gemini_text = gemini_generate(prompt)
    if gemini_text:
        return gemini_text

    if intent == "trend":
        return "Current trends: oversized streetwear, neutral tones, and minimalist fashion."

    return "I can help you with outfit recommendations and fashion trends."


if __name__ == "__main__":
    query = input("Enter your query: ")
    print(generate_response(query))