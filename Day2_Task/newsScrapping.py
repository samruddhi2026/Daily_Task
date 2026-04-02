import json
import os
import re
import time

import requests


current_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(current_folder)
env_file_path = os.path.join(root_folder, ".env")
config_file_path = os.path.join(current_folder, "category_config.json")
output_file_path = os.path.join(current_folder, "output.json")

search_keyword = "Global Economy"


def load_api_key():
    if not os.path.exists(env_file_path):
        return None

    with open(env_file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line.startswith("NEWS_API"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    return parts[1].strip().strip('"').strip("'")

    return None


class NewsClassifier:
    def __init__(self, config_path):
        with open(config_path, "r", encoding="utf-8") as file:
            self.config_data = json.load(file)

        self.category_keywords = {
            "FINANCE": self.config_data.get("FINANCE", []),
            "TECH": self.config_data.get("TECH", []),
            "POLITICS": self.config_data.get("POLITICS", []),
            "GENERAL": self.config_data.get("GENERAL", [])
        }
        self.tech_companies = self.config_data.get("TECH_COMPANIES", [])
        self.finance_companies = self.config_data.get("FINANCE_COMPANIES", [])

    def classify(self, headline):
        words = re.findall(r"[a-z]+", headline.lower())
        best_category = "GENERAL"
        best_score = 0

        for category, keywords in self.category_keywords.items():
            score = 0

            for keyword in keywords:
                if keyword.lower() in words:
                    score = score + 1

            if score > best_score:
                best_score = score
                best_category = category

        return best_category


def get_company_list(category, classifier):
    if category == "TECH":
        return classifier.tech_companies
    if category == "FINANCE":
        return classifier.finance_companies
    return classifier.tech_companies + classifier.finance_companies


def extract_entities(headline, description, company_list):
    if headline is None:
        headline = ""
    if description is None:
        description = ""

    companies = []
    text = (headline + " " + description).lower()

    for company in company_list:
        if company.lower() in text and company not in companies:
            companies.append(company)

    percentages = re.findall(r"\b\d+(?:\.\d+)?%", description)
    currency = re.findall(r"\$\d+(?:\.\d+)?|Rs\.?\s?\d+(?:\.\d+)?|INR\s?\d+(?:\.\d+)?", description)

    return {
        "companies": companies,
        "percentages": percentages,
        "currency": currency
    }


def fetch_articles(api_key):
    url = "https://newsdata.io/api/1/latest"
    params = {
        "apikey": api_key,
        "q": search_keyword,
        "language": "en"
    }

    tries = 0

    while tries < 3:
        try:
            response = requests.get(url, params=params, timeout=15)
        except requests.exceptions.Timeout:
            wait_time = 2 ** tries
            time.sleep(wait_time)
            tries = tries + 1
            continue
        except requests.exceptions.RequestException:
            return []

        if response.status_code == 429:
            wait_time = 2 ** tries
            time.sleep(wait_time)
            tries = tries + 1
        elif response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("results", [])[:50]
            return []
        else:
            return []

    return []


def build_output(articles, classifier):
    final_output = []
    seen_headlines = set()

    for article in articles:
        headline = article.get("title")
        description = article.get("description")

        if not headline:
            continue

        clean_headline = headline.strip().lower()
        if clean_headline in seen_headlines:
            continue

        seen_headlines.add(clean_headline)

        category = classifier.classify(headline)

        news_item = {
            "headline": headline,
            "category": category,
            "entities": extract_entities(headline, description, get_company_list(category, classifier))
        }

        final_output.append(news_item)

    return final_output


def main():
    api_key = load_api_key()

    if not api_key:
        print("API key not found")
        return

    classifier = NewsClassifier(config_file_path)
    articles = fetch_articles(api_key)
    final_output = build_output(articles, classifier)

    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(final_output, file, indent=4, ensure_ascii=False)

    print("Total articles fetched:", len(final_output))
    print("Data stored in output.json")


if __name__ == "__main__":
    main()
