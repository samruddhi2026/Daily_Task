class IntentRouter:
    def route(self, query):
        query = query.lower()

        recommendation_keywords = ["outfit", "style", "wear", "vibe", "minimal", "look", "fashion", "clothes", "wardrobe", "party", "top", "bottom", "piece", "ensemble"]
        if any(word in query for word in recommendation_keywords):
            return "recommendation"

        elif "trend" in query:
            return "trend"

        else:
            return "general"