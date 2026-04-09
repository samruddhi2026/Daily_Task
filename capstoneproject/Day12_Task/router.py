class IntentRouter:
    def route(self, query):
        query = query.lower()

        if "outfit" in query or "style" in query or "wear" in query:
            return "recommendation"

        elif "trend" in query:
            return "trend"

        else:
            return "general"