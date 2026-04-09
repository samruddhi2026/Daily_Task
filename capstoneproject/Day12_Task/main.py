from Day11_Task.retriever import retrieve
from Day12_Task.router import IntentRouter
from Day12_Task.prompts import PROMPTS

def safety_check(query):
    banned = ["hate", "offensive", "abuse"]
    return not any(word in query.lower() for word in banned)

def generate_response(query):
    
    if not safety_check(query):
        return "Sorry, I cannot respond to that request."

    
    router = IntentRouter()
    intent = router.route(query)

    
    prompt = PROMPTS[intent]

    
    if intent == "recommendation":
        results = retrieve(query)

        output = "Recommended Outfit:\n"
        for item in results:
            output += f"- {item['text']} ({item['style_vibe']})\n"

        return output

    elif intent == "trend":
        return "Current trends include oversized streetwear, neutral tones, and minimalist outfits."

    else:
        return "I can help you with outfit recommendations and fashion trends."

if __name__ == "__main__":
    query = input("Enter your query: ")
    print(generate_response(query))