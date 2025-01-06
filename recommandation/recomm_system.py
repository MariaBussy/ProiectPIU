import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Function to load data from a JSON file
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        print(f"Successfully loaded {len(data)} books.")
        return data
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return []
    except FileNotFoundError:
        print("File not found.")
        return []

# Function to recommend books based on multiple given titles
def recommend_books(input_titles, data, top_n=3, description_weight=1, genre_weight=3, max_description_length=300):
    # Ensure data is not empty
    if not data:
        return "No data available to make recommendations."

    # Combine genre and description fields with weights
    for book in data:
        # Normalize the description length
        truncated_description = book['description'][:max_description_length]
        weighted_genre = ' '.join(book['genre']) * genre_weight
        weighted_description = truncated_description * description_weight
        book['combined'] = f"{weighted_genre} {weighted_description}"

    # Prepare data for similarity computation
    combined_texts = [book['combined'] for book in data]
    vectorizer = TfidfVectorizer().fit_transform(combined_texts)
    similarity_matrix = cosine_similarity(vectorizer)

    # Find indices of input books
    target_indices = [
        i for i, book in enumerate(data) if book['title'] in input_titles
    ]
    if not target_indices:
        return f"No matching books found for input titles: {input_titles}"

    # Average similarity scores across all input books
    avg_similarity_scores = np.mean(similarity_matrix[target_indices], axis=0)

    # Sort scores and exclude the input books
    similarity_scores = list(enumerate(avg_similarity_scores))
    similarity_scores = sorted(
        similarity_scores, key=lambda x: x[1], reverse=True
    )
    similarity_scores = [
        (data[i]['title'], data[i]['author'], score)
        for i, score in similarity_scores
        if data[i]['title'] not in input_titles
    ]

    # Get top N recommendations
    recommendations = similarity_scores[:top_n]
    return recommendations

# Main function
if __name__ == "__main__":
    # Load the JSON file
    file_path = "dataset.json"  # Replace with the path to your JSON file
    books_data = load_json(file_path)

    # Example: Get recommendations for multiple books with adjusted weights
    input_books = ["1984", "Pride and Prejudice", "Harry Potter and the Sorcerer's Stone"]
    recommended_books = recommend_books(
        input_books, books_data,
        description_weight=1, genre_weight=5, max_description_length=300
    )
    print(f"Books recommended for {input_books}:")
    for title, author, score in recommended_books:
        print(f"  - {title} by {author} (Similarity Score: {score:.2f})")
