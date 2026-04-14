import time
from Day12_Task.main import generate_response
from Day11_Task.retriever import retrieve

test_queries = [
    "minimalist outfit",
    "edgy streetwear",
    "casual daily outfit",
    "latest fashion trends",
    "sporty outfit",
    "formal outfit",
    "what should I wear",
    "summer outfit",
    "winter street style",
    "black outfit ideas"
]

def benchmark():
    print("\n PERFORMANCE TESTING STARTED \n")

    total_time = 0

    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")

       
        start_retrieval = time.time()
        retrieve(query)
        retrieval_time = time.time() - start_retrieval

       
        start_total = time.time()
        response = generate_response(query)
        total_query_time = time.time() - start_total

        total_time += total_query_time

        print(f"Retrieval Time: {retrieval_time:.4f} sec")
        print(f"Total Time: {total_query_time:.4f} sec")
        print("-" * 50)

    avg_time = total_time / len(test_queries)

    print("\n FINAL RESULTS")
    print(f"Average Response Time: {avg_time:.4f} sec")


if __name__ == "__main__":
    benchmark()