import json

import requests

# Function to load data from a JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Example usage
file_path = 'books.json'  # Specify the path to your JSON file
data = load_json_data(file_path)

# Function to make GET request to Google Books API
def get_book_info(book_name, author_name, api_key):
    query = f"{book_name}+inauthor:{author_name}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"

    # Send the GET request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and return the JSON response
        return response.json()
    else:
        # If request failed, print the error
        return f"Error: {response.status_code}"

api_key = "AIzaSyBx5Psf4RSTDW8Br_dWkc8618JkFIMkFYQ"  # Replace with your Google Books API key

complete_info=[]
for book in data:
    book_data=get_book_info(book['title'],  book['author'], api_key)
    book_description=''
    preview_link = ''
    for i in range (len(book_data['items'])):
        if book_data['items'][i]['volumeInfo']['description'] and book_description=='' and book_data['items'][i]['volumeInfo']['previewLink'] and preview_link=='':
            book_description=book_data['items'][i]['volumeInfo']['description']
            preview_link=book_data['items'][i]['volumeInfo']['previewLink']
            break
    complete_info.append({
        'title': book_data['items'][0]['volumeInfo']['title'],
        'author': book_data['items'][0]['volumeInfo']['authors'],
        'description': book_description,
        'preview_link': preview_link
    })

file_path = 'dataset.json'
with open(file_path, 'w') as file:
    json.dump(complete_info, file, indent=4)
