import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import unicodedata
import random


class RecommendationSystem:
    def __init__(self, dataset_path="./recommandation/dataset.json"):
        self.books_dataset=self.load_json(dataset_path)
        self.description_weight = 1
        self.genre_weight = 3
        self.max_description_length = 300
        self.books_data = self.load_booksdata()

    @staticmethod
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

    @staticmethod
    def normalize_text(text):
        text = text.replace('’', "'").replace('\u2019', "'")
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').strip()

    def load_booksdata(self):
        books_data=[]
        # Ensure data is not empty
        if not self.books_dataset:
            print("No data available to make recommendations. Load a dataset!")
            raise Exception("No dataset")

        # Combine genre and description fields with weights
        for book in self.books_dataset:
            # Normalize the description length
            truncated_description = book['description'][:self.max_description_length]
            weighted_genre = ' '.join(book['genre']) * self.genre_weight
            weighted_description = truncated_description * self.description_weight
            book["title"]=self.normalize_text(book["title"])
            book['combined'] = f"{weighted_genre} {weighted_description}"
            books_data.append(book)

        return books_data

    def recommend_random(self, top_n):
        random_books = random.sample(self.books_data, min(top_n, len(self.books_data)))
        return [{'title': book['title'], 'author': book['author'], 'preview_link': book['preview_link']} for book in random_books]

    # Function to recommend books based on multiple given titles
    def recommend_books(self, input_titles, top_n=3):
        if not input_titles:
            return self.recommend_random(top_n)

        # Prepare data for similarity computation
        combined_texts = [book['combined'] for book in self.books_data]
        vectorizer = TfidfVectorizer().fit_transform(combined_texts)
        similarity_matrix = cosine_similarity(vectorizer)

        normalized_input_titles = [self.normalize_text(title) for title in input_titles]

        # Find indices of input books
        target_indices = [
            i for i, book in enumerate(self.books_data) if book['title'] in normalized_input_titles
        ]
        if not target_indices:
            print(f"No matching books found for input titles: {normalized_input_titles}")
            return self.recommend_random(top_n)

        # Average similarity scores across all input books
        avg_similarity_scores = np.mean(similarity_matrix[target_indices], axis=0)

        # Sort scores and exclude the input books
        similarity_scores = list(enumerate(avg_similarity_scores))
        similarity_scores = sorted(
            similarity_scores, key=lambda x: x[1], reverse=True
        )

        # To avoid repeating book titles, we'll keep track of recommended titles
        recommended_titles = set()
        recommendations = []

        for i, score in similarity_scores:
            book = self.books_data[i]
            if book['title'] not in input_titles and book['title'] not in recommended_titles:
                recommended_titles.add(book['title'])
                recommendations.append((book['title'], book['author'], book['preview_link']))

            if len(recommendations) >= top_n:
                break

        # Format recommendations into the final dictionary format
        recommendations_dict = [{'title': title, 'author': author, 'preview_link': preview_link}
                                for title, author, preview_link in recommendations]
        return recommendations_dict