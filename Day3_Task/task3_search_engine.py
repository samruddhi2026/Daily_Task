import string


stopwords = ["the", "is", "at", "on", "in", "and", "a", "of", "to", "for", "with", "by", "an"]


def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return set(words)


def jaccard_similarity(set1, set2):
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    if len(union) == 0:
        return 0
    return len(intersection) / len(union)


def load_corpus(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    sentences = [line.strip() for line in lines if line.strip()]
    return sentences


def search(query, sentences):
    query_tokens = preprocess_text(query)
    
    scores = []
    
    for sentence in sentences:
        sentence_tokens = preprocess_text(sentence)
        score = jaccard_similarity(query_tokens, sentence_tokens)
        scores.append((sentence, score))
    
   
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return scores


if __name__ == "__main__":
    file_path = "corpus.txt"
    sentences = load_corpus(file_path)
    
    query = input("Enter your search query: ")
    
    results = search(query, sentences)
    
    print("\nTop Results:\n")
    for sentence, score in results[:5]:
        print(f"{round(score, 2)} -> {sentence}")