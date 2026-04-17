import os
import requests
import json
import base64
import urllib.parse
import time
import random
import re

from Day11_Task.retriever import retrieve
from Day12_Task.router import IntentRouter
from Day12_Task.prompts import PROMPTS


# -------------------- ENV LOADER --------------------
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


# -------------------- DATA CACHE --------------------
_wardrobe_cache = None

def get_wardrobe():
    global _wardrobe_cache
    if _wardrobe_cache is None:
        try:
            data_path = os.path.join(os.path.dirname(__file__), '..', 'Day11_Task', 'data.json')
            if os.path.exists(data_path):
                with open(data_path, 'r', encoding='utf-8') as f:
                    _wardrobe_cache = json.load(f)
            else:
                _wardrobe_cache = []
        except Exception:
            _wardrobe_cache = []
    return _wardrobe_cache


# -------------------- SAFETY --------------------
def safety_check(query):
    banned = ["hate", "offensive", "abuse", "illegal"]
    if any(word in query.lower() for word in banned):
        return False
    if len(query.strip()) < 3:
        return False
    return True


# -------------------- JSON CLEANER --------------------
def extract_json_block(text):
    if not text:
        return None
    try:
        temp = text.strip()

        if "```json" in temp:
            temp = temp.split("```json")[-1].split("```")[0].strip()
        elif "```" in temp:
            temp = temp.split("```")[-1].split("```")[0].strip()

        start = temp.find("{")
        end = temp.rfind("}")

        if start != -1 and end != -1:
            potential_json = temp[start:end + 1]
            try:
                json.loads(potential_json)
                return potential_json
            except:
                blocks = re.findall(r'\{.*\}', temp, re.DOTALL)
                for block in reversed(blocks):
                    try:
                        json.loads(block)
                        return block
                    except:
                        continue
    except Exception:
        pass
    return None


# -------------------- TEXT GENERATION --------------------
def gemini_generate(prompt):
    try:
        seed = random.randint(1, 100000)
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://text.pollinations.ai/openai/{encoded_prompt}?seed={seed}&json=true"
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            return response.text.strip()

        return None
    except Exception:
        return None


# -------------------- IMAGE GENERATION --------------------
def hf_generate_image(prompt, retries=3):
    try:
        seed = random.randint(1, 100000)
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&nologo=true&model=flux&seed={seed}"

        for _ in range(retries):
            try:
                res = requests.get(url, timeout=40)
                if res.status_code == 200 and len(res.content) > 5000:
                    return base64.b64encode(res.content).decode("utf-8"), None
                time.sleep(1)
            except:
                pass
    except:
        pass

    # Fallback: Eden AI
    api_key = os.getenv("IMAGE_API_KEY")
    if api_key:
        try:
            url = "https://api.edenai.run/v2/image/generation"
            headers = {"Authorization": f"Bearer {api_key}"}
            payload = {
                "providers": "stabilityai",
                "text": prompt,
                "resolution": "512x512",
                "num_images": 1
            }
            res = requests.post(url, json=payload, headers=headers, timeout=20)

            if res.status_code == 200:
                img_url = res.json().get("stabilityai", {}).get("items", [{}])[0].get("image_resource_url")
                if img_url:
                    img_data = requests.get(img_url, timeout=15).content
                    return base64.b64encode(img_data).decode("utf-8"), None
        except:
            pass

    return None, "All image engines failed."


# -------------------- COLOR FILTER --------------------
def get_color_matches(query):
    colors = ["red", "blue", "green", "white", "black", "grey", "beige", "multi",
              "pink", "navy", "brown", "khaki", "silver", "gold"]

    l_query = query.lower()
    found_colors = [c for c in colors if c in l_query]

    if not found_colors:
        return []

    wardrobe = get_wardrobe()
    return [
        item for item in wardrobe
        if item.get('color', '').lower() in found_colors
    ]


# -------------------- REMOVE DUPLICATES --------------------
def remove_duplicates(items):
    seen = set()
    unique = []

    for item in items:
        key = json.dumps(item, sort_keys=True)
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique


# -------------------- MAIN FUNCTION --------------------
def generate_response(query):
    if not safety_check(query):
        return json.dumps({"error": "Safety check failed"})

    router = IntentRouter()
    intent = router.route(query)

    if intent == "recommendation":

        results = retrieve(query)
        color_hits = get_color_matches(query)

        # ✅ FIXED: remove duplicates
        combined = remove_duplicates(color_hits + results)

        random.shuffle(combined)
        results = combined[:8]

        base_prompt = PROMPTS.get("recommendation")

        l_query = query.lower()

        # Gender
        if any(w in l_query for w in ["woman", "lady", "female", "girl"]):
            gender = "female"
        elif any(w in l_query for w in ["man", "male", "guy", "boy"]):
            gender = "male"
        else:
            gender = "neutral"

        # Lighting
        if any(w in l_query for w in ["party", "glam", "night"]):
            lighting_style = "Dramatic high-contrast lighting with golden hour accents and glossy reflections"
        elif any(w in l_query for w in ["minimal", "clean"]):
            lighting_style = "Ultra-clean minimal studio lighting, crisp shadows"
        else:
            lighting_style = "Soft diffused lighting"

        # Silhouette
        if gender == "female":
            silhouette_style = "High-fashion female silhouette, graceful elegant pose, centered"
        elif gender == "male":
            silhouette_style = "Strong masculine silhouette, confident upright pose, centered"
        else:
            silhouette_style = "front-facing mannequin, centered"

        # Context
        items_context = "\n".join([
            f"- {i.get('text','')} (Style: {i.get('style_vibe','')}, Category: {i.get('category','')})"
            for i in results
        ])

        final_prompt = base_prompt.format(
            user_input=query,
            retrieved_items=items_context,
            gender=gender
        )

        final_prompt = final_prompt.replace(
            "Soft diffused lighting with natural shadows.",
            lighting_style
        )

        final_prompt = final_prompt.replace(
            "front-facing mannequin, centered.",
            silhouette_style
        )

        final_prompt = final_prompt.replace("{{gender}}", gender)

        raw_text = gemini_generate(final_prompt)
        clean_json = extract_json_block(raw_text)

        return clean_json if clean_json else json.dumps({"error": "Failed to extract outfit data"})

    # General case
    prompt = PROMPTS.get(intent, PROMPTS["general"])
    return gemini_generate(prompt)

