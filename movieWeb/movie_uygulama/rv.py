import requests
import random
from nltk.tokenize import word_tokenize
import nltk
from nltk.corpus import stopwords
import re
import random
import joblib
import os
from django.conf import settings
from . import config
from difflib import SequenceMatcher
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from datetime import datetime
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


# ----------------------------
# state
# ----------------------------
state = {"step": 6, "selection": None, "suggestion": None}
chat_history_ids = None
# ----------------------------
# Models and Vectorizers
# ----------------------------
classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
model111 = SentenceTransformer('all-MiniLM-L6-v2')

model222 = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
tokenizer222 = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")

classifier444 = pipeline("zero-shot-classification", 
                     model="typeform/distilbert-base-uncased-mnli",
                     device=0 if torch.cuda.is_available() else -1)

current_dir = os.path.dirname(os.path.abspath(__file__))

# Dosya yollarını oluşturur
saved_model_path = os.path.join(current_dir, "saved_model3.pkl")
saved_vectorizer_path = os.path.join(current_dir, "vectorizer3.pkl")

clf = joblib.load(saved_model_path)
vectorizer = joblib.load(saved_vectorizer_path)



# ----------------------------
# CONFİG DATA
# ----------------------------
# API Anahtarları
TMDB_API_KEY = config.TMDB_API_KEY
GOOGLE_BOOKS_API_KEY = config.GOOGLE_BOOKS_API_KEY
# Film Kategorileri
CATEGORY_NAMES_MOVIE = config.CATEGORY_NAMES_MOVIE
# Dizi Kategorileri
CATEGORY_NAMES_TV = config.CATEGORY_NAMES_TV
# Kitap Kategorileri
CATEGORY_NAMES_BOOKS = config.CATEGORY_NAMES_BOOKS
# Konular
konular = config.konular
# Temel Yanıtlar
acceptances = config.acceptances
rejections = config.rejections
greetings_sentences = config.greetings_sentences
stop_sentences = config.stop_sentences
curse_sentences = config.curse_sentences
reset_sentences = config.reset_sentences
previous_sentences = config.previous_sentences
sexual_sentences = config.sexual_content
# Kullanıcı Yanıtları
rejection_responses = config.rejection_responses
acceptance_responses = config.acceptance_responses
start_responses = config.start_responses
start_responses_short = config.start_responses_short
greeting_responses = config.greeting_responses
stop_responses = config.stop_responses
curse_responses = config.curse_responses
reset_responses = config.reset_responses
invalid_responses = config.invalid_responses
previous_responses = config.previous_responses
clarification_responses = config.clarification_responses
resume_responses = config.resume_responses
sexual_content_responses = config.sexual_content_responses
describe_responses = config.describe_responses
ask_movie_type = config.ask_movie_type
ask_serie_type = config.ask_serie_type
ask_book_type = config.ask_book_type
movie_category_keywords = config.movie_category_keywords
tv_category_keywords = config.tv_category_keywords
book_category_keywords = config.book_category_keywords




# ==================================
#  1) Film Öneri Fonksiyonları
# ==================================
def recommend_movie_one_category(category_name):
    category_id = CATEGORY_NAMES_MOVIE.get(category_name)
    if not category_id:
        state["step"] = 2
        return random.choice(invalid_responses)

    today = datetime.today()
    three_years_ago = today.replace(year=today.year - 3, month=1, day=1)

    # URL seçimi
    if state["suggestion"] == "high":
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={category_id}&language=en-US&vote_average.gte=7"
        )
    elif state["suggestion"] == "new":
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={category_id}&language=en-US"
            f"&primary_release_date.gte={three_years_ago.strftime('%Y-%m-%d')}"
            f"&primary_release_date.lte={today.strftime('%Y-%m-%d')}"
        )
    elif state["suggestion"] == "bad":
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={category_id}&language=en-US&vote_average.lte=5"
        )
    else:
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={category_id}&language=en-US"
        )

    movies = []
    for attempt in range(16):
        response = requests.get(url).json()
        total_pages = response.get("total_pages", 1)
        random_page = random.randint(1, total_pages)
        url_with_page = f"{url}&page={random_page}"
        movies = requests.get(url_with_page).json().get("results", [])
        if movies:
            break

    if movies:
        movie = random.choice(movies)

        global description, year, cast, director, title
        title = movie.get('title', 'Title not available')
        year = movie.get('release_date', 'Year not available')[:4]
        credits_url = f"https://api.themoviedb.org/3/movie/{movie.get('id')}/credits?api_key={TMDB_API_KEY}&language=en-US"
        credits_response = requests.get(credits_url).json()
        cast = [member['name'] for member in credits_response.get('cast', [])][:5] or ['Cast not available']
        director = next((member['name'] for member in credits_response.get('crew', []) if member['job'] == 'Director'), 'Director not found')
        description = movie.get('overview', 'I do not have information about this movie.')

        return f"Recommended Movie: {movie.get('title')} <br>{random.choice(describe_responses)}"
    state["step"] = 2
    return "No movies found for this category."


def recommend_movie_two_categories(category1, category2):
    category_id1 = CATEGORY_NAMES_MOVIE.get(category1)
    category_id2 = CATEGORY_NAMES_MOVIE.get(category2)
    if not category_id1 or not category_id2:
        state["step"] = 2
        return random.choice(invalid_responses)

    genres = f"{category_id1},{category_id2}"

    today = datetime.today()
    three_years_ago = today.replace(year=today.year - 3, month=1, day=1)

    if state["suggestion"] == "high":
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US&vote_average.gte=7"
        )
    elif state["suggestion"] == "new":
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US"
            f"&primary_release_date.gte={three_years_ago.strftime('%Y-%m-%d')}"
            f"&primary_release_date.lte={today.strftime('%Y-%m-%d')}"
        )
    elif state["suggestion"] == "bad":
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US&vote_average.lte=5"
        )
    else:
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US"
        )

    movies = []
    for attempt in range(18):
        response = requests.get(url).json()
        total_pages = response.get("total_pages", 1)
        random_page = random.randint(1, total_pages)
        url_with_page = f"{url}&page={random_page}"
        movies = requests.get(url_with_page).json().get("results", [])
        if movies:
            break

    if movies:
        movie = random.choice(movies)

        global description, year, cast, director, title
        title = movie.get('title', 'Title not available')
        year = movie.get('release_date', 'Year not available')[:4]
        credits_url = f"https://api.themoviedb.org/3/movie/{movie.get('id')}/credits?api_key={TMDB_API_KEY}&language=en-US"
        credits_response = requests.get(credits_url).json()
        cast = [member['name'] for member in credits_response.get('cast', [])][:5] or ['Cast not available']
        director = next((member['name'] for member in credits_response.get('crew', []) if member['job'] == 'Director'), 'Director not found')
        description = movie.get('overview', 'I do not have information about this movie.')

        return f"Recommended Movie: {movie.get('title')} <br>{random.choice(describe_responses)}"
    state["step"] = 2
    return "No movies found for these categories."


def recommend_movie_three_categories(category1, category2, category3):
    category_id1 = CATEGORY_NAMES_MOVIE.get(category1)
    category_id2 = CATEGORY_NAMES_MOVIE.get(category2)
    category_id3 = CATEGORY_NAMES_MOVIE.get(category3)
    if not category_id1 or not category_id2 or not category_id3:
        state["step"] = 2
        return random.choice(invalid_responses)

    genres = f"{category_id1},{category_id2},{category_id3}"

    today = datetime.today()
    three_years_ago = today.replace(year=today.year - 3, month=today.month, day=1)

    if state["suggestion"] == "high":
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US&vote_average.gte=7"
        )
    elif state["suggestion"] == "new":
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US"
            f"&primary_release_date.gte={three_years_ago.strftime('%Y-%m-%d')}"
            f"&primary_release_date.lte={today.strftime('%Y-%m-%d')}"
        )
    elif state["suggestion"] == "bad":
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US&vote_average.lte=5"
        )
    else:
        url = (
            f"https://api.themoviedb.org/3/discover/movie?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US"
        )

    movies = []
    for attempt in range(20):
        response = requests.get(url).json()
        total_pages = response.get("total_pages", 1)
        random_page = random.randint(1, total_pages)
        url_with_page = f"{url}&page={random_page}"
        movies = requests.get(url_with_page).json().get("results", [])
        if movies:
            break

    if movies:
        movie = random.choice(movies)

        global description, year, cast, director, title
        title = movie.get('title', 'Title not available')
        year = movie.get('release_date', 'Year not available')[:4]
        credits_url = f"https://api.themoviedb.org/3/movie/{movie.get('id')}/credits?api_key={TMDB_API_KEY}&language=en-US"
        credits_response = requests.get(credits_url).json()
        cast = [member['name'] for member in credits_response.get('cast', [])][:5] or ['Cast not available']
        director = next((member['name'] for member in credits_response.get('crew', []) if member['job'] == 'Director'), 'Director not found')
        description = movie.get('overview', 'I do not have information about this movie.')

        return f"Recommended Movie: {movie.get('title')} <br>{random.choice(describe_responses)}"
    state["step"] = 2
    return "No movies found for these categories."


# ==================================
#  2) Dizi (TV) Öneri Fonksiyonları
# ==================================
def recommend_tv_one_category(category_name):
    category_id = CATEGORY_NAMES_TV.get(category_name)
    if not category_id:
        state["step"] = 2
        return random.choice(invalid_responses)

    today = datetime.today()
    three_years_ago = today.replace(year=today.year - 3, month=1, day=1)

    # URL seçimi
    if state["suggestion"] == "high":
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={category_id}&language=en-US&vote_average.gte=7"
        )
    elif state["suggestion"] == "new":
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={category_id}&language=en-US"
            f"&first_air_date.gte={three_years_ago.strftime('%Y-%m-%d')}"
            f"&first_air_date.lte={today.strftime('%Y-%m-%d')}"
        )
    elif state["suggestion"] == "bad":
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={category_id}&language=en-US&vote_average.lte=5"
        )
    else:
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={category_id}&language=en-US"
        )

    tv_shows = []
    for attempt in range(16):
        response = requests.get(url).json()
        total_pages = response.get("total_pages", 1)
        random_page = random.randint(1, total_pages)
        url_with_page = f"{url}&page={random_page}"
        tv_shows = requests.get(url_with_page).json().get("results", [])
        if tv_shows:
            break

    if tv_shows:
        show = random.choice(tv_shows)

        global description, year, cast, director, title
        title = show.get('name', 'Title not available')
        year = show.get('first_air_date', 'Year not available')[:4]
        credits_url = f"https://api.themoviedb.org/3/tv/{show.get('id')}/credits?api_key={TMDB_API_KEY}&language=en-US"
        credits_response = requests.get(credits_url).json()
        cast = [member['name'] for member in credits_response.get('cast', [])][:5] or ['Cast not available']
        director = next((member['name'] for member in credits_response.get('crew', []) if member['job'] == 'Director'), 'Director not found')
        description = show.get('overview', 'I do not have information about this TV show.')

        return f"Recommended TV Show: {show.get('name')} <br>{random.choice(describe_responses)}"
    state["step"] = 2
    return "No TV shows found for this category."


def recommend_tv_two_categories(category1, category2):
    category_id1 = CATEGORY_NAMES_TV.get(category1)
    category_id2 = CATEGORY_NAMES_TV.get(category2)
    if not category_id1 or not category_id2:
        state["step"] = 2
        return random.choice(invalid_responses)

    genres = f"{category_id1},{category_id2}"

    today = datetime.today()
    three_years_ago = today.replace(year=today.year - 3, month=1, day=1)

    if state["suggestion"] == "high":
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US&vote_average.gte=7"
        )
    elif state["suggestion"] == "new":
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US"
            f"&first_air_date.gte={three_years_ago.strftime('%Y-%m-%d')}"
            f"&first_air_date.lte={today.strftime('%Y-%m-%d')}"
        )
    elif state["suggestion"] == "bad":
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US&vote_average.lte=5"
        )
    else:
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US"
        )

    tv_shows = []
    for attempt in range(18):
        response = requests.get(url).json()
        total_pages = response.get("total_pages", 1)
        random_page = random.randint(1, total_pages)
        url_with_page = f"{url}&page={random_page}"
        tv_shows = requests.get(url_with_page).json().get("results", [])
        if tv_shows:
            break

    if tv_shows:
        show = random.choice(tv_shows)

        global description, year, cast, director, title
        title = show.get('name', 'Title not available')
        year = show.get('first_air_date', 'Year not available')[:4]
        credits_url = f"https://api.themoviedb.org/3/tv/{show.get('id')}/credits?api_key={TMDB_API_KEY}&language=en-US"
        credits_response = requests.get(credits_url).json()
        cast = [member['name'] for member in credits_response.get('cast', [])][:5] or ['Cast not available']
        director = next((member['name'] for member in credits_response.get('crew', []) if member['job'] == 'Director'), 'Director not found')
        description = show.get('overview', 'I do not have information about this TV show.')

        return f"Recommended TV Show: {show.get('name')} <br>{random.choice(describe_responses)}"
    state["step"] = 2
    return "No TV shows found for these categories."


def recommend_tv_three_categories(category1, category2, category3):
    category_id1 = CATEGORY_NAMES_TV.get(category1)
    category_id2 = CATEGORY_NAMES_TV.get(category2)
    category_id3 = CATEGORY_NAMES_TV.get(category3)
    if not category_id1 or not category_id2 or not category_id3:
        state["step"] = 2
        return random.choice(invalid_responses)

    genres = f"{category_id1},{category_id2},{category_id3}"

    today = datetime.today()
    three_years_ago = today.replace(year=today.year - 3, month=1, day=1)

    if state["suggestion"] == "high":
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US&vote_average.gte=7"
        )
    elif state["suggestion"] == "new":
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US"
            f"&first_air_date.gte={three_years_ago.strftime('%Y-%m-%d')}"
            f"&first_air_date.lte={today.strftime('%Y-%m-%d')}"
        )
    elif state["suggestion"] == "bad":
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US&vote_average.lte=5"
        )
    else:
        url = (
            f"https://api.themoviedb.org/3/discover/tv?"
            f"api_key={TMDB_API_KEY}&with_genres={genres}&language=en-US"
        )

    tv_shows = []
    for attempt in range(20):
        response = requests.get(url).json()
        total_pages = response.get("total_pages", 1)
        random_page = random.randint(1, total_pages)
        url_with_page = f"{url}&page={random_page}"
        tv_shows = requests.get(url_with_page).json().get("results", [])
        if tv_shows:
            break

    if tv_shows:
        show = random.choice(tv_shows)

        global description, year, cast, director, title
        title = show.get('name', 'Title not available')
        year = show.get('first_air_date', 'Year not available')[:4]
        credits_url = f"https://api.themoviedb.org/3/tv/{show.get('id')}/credits?api_key={TMDB_API_KEY}&language=en-US"
        credits_response = requests.get(credits_url).json()
        cast = [member['name'] for member in credits_response.get('cast', [])][:5] or ['Cast not available']
        director = next((member['name'] for member in credits_response.get('crew', []) if member['job'] == 'Director'), 'Director not found')
        description = show.get('overview', 'I do not have information about this TV show.')

        return f"Recommended TV Show: {show.get('name')} <br>{random.choice(describe_responses)}"
    state["step"] = 2
    return "No TV shows found for these categories."


# ==================================
#  3) Kitap Öneri Fonksiyonları
# ==================================

def recommend_book_one_category(category_name):
    category_id = CATEGORY_NAMES_BOOKS.get(category_name)
    if not category_id:
        state["step"] = 2
        return random.choice(invalid_responses)

    today = datetime.today()
    three_years_ago = today.replace(year=today.year - 3)

    if state["suggestion"] == "high":
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q=subject:{category_id}&key={GOOGLE_BOOKS_API_KEY}"
        ).json()
        total_items = response.get("totalItems", 100)
        start_index = random.randint(0, max(total_items - 20, 0))

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q=subject:{category_id}"
            f"&startIndex={start_index}"
            f"&maxResults=20"
            f"&key={GOOGLE_BOOKS_API_KEY}"
        )

    elif state["suggestion"] == "new":
        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q=subject:{category_id}+publishedDate:{three_years_ago.strftime('%Y')}-{today.strftime('%Y')}"
            f"&maxResults=20"
            f"&orderBy=newest"
            f"&key={GOOGLE_BOOKS_API_KEY}"
        )
    elif state["suggestion"] == "bad":
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q=subject:{category_id}&key={GOOGLE_BOOKS_API_KEY}"
        ).json()
        total_items = response.get("totalItems", 100)
        start_index = random.randint(0, max(total_items - 20, 0))

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q=subject:{category_id}"
            f"&startIndex={start_index}"
            f"&maxResults=20"
            f"&key={GOOGLE_BOOKS_API_KEY}"
            f"&filter=free-ebooks"
        )
    else:
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q=subject:{category_id}&key={GOOGLE_BOOKS_API_KEY}"
        ).json()
        total_items = response.get("totalItems", 100)
        start_index = random.randint(0, max(total_items - 20, 0))

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q=subject:{category_id}"
            f"&startIndex={start_index}"
            f"&maxResults=20"
            f"&key={GOOGLE_BOOKS_API_KEY}"
        )

    items = []
    for attempt in range(16):
        response = requests.get(url).json()
        items = response.get("items", [])
        if items:
            break

    if not items:
        state["step"] = 2
        return "No books found for this category."

    book = random.choice(items)
    volume_info = book.get("volumeInfo", {})
    
    global description, year, publisher, authors, title
    description = volume_info.get("description", "I do not have information about this book.")
    year = volume_info.get("publishedDate", "Year not available")[:4]
    publisher = volume_info.get("publisher", "Publisher not available")
    title = volume_info.get("title", "Unknown Title")
    authors = volume_info.get("authors", ["Unknown Author"])

    return f"Recommended Book: '{title}' by {', '.join(authors)} <br>{random.choice(describe_responses)}"


def recommend_book_two_categories(category1, category2):
    category_id1 = CATEGORY_NAMES_BOOKS.get(category1)
    category_id2 = CATEGORY_NAMES_BOOKS.get(category2)
    if not category_id1 or not category_id2:
        state["step"] = 2
        return random.choice(invalid_responses)

    today = datetime.today()
    three_years_ago = today.replace(year=today.year - 3)

    query = f"subject:{category_id1}+subject:{category_id2}"

    if state["suggestion"] == "high":
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
        ).json()
        total_items = response.get("totalItems", 100)
        start_index = random.randint(0, max(total_items - 20, 0))

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q={query}"
            f"&startIndex={start_index}"
            f"&maxResults=20"
            f"&key={GOOGLE_BOOKS_API_KEY}"
        )

    elif state["suggestion"] == "new":
        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q={query}+publishedDate:{three_years_ago.strftime('%Y')}-{today.strftime('%Y')}"
            f"&maxResults=20"
            f"&orderBy=newest"
            f"&key={GOOGLE_BOOKS_API_KEY}"
        )
    elif state["suggestion"] == "bad":
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q=subject:{query}&key={GOOGLE_BOOKS_API_KEY}"
        ).json()
        total_items = response.get("totalItems", 100)
        start_index = random.randint(0, max(total_items - 20, 0))

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q=subject:{query}"
            f"&startIndex={start_index}"
            f"&maxResults=20"
            f"&key={GOOGLE_BOOKS_API_KEY}"
            f"&filter=free-ebooks"
        )
    else:
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
        ).json()
        total_items = response.get("totalItems", 100)
        start_index = random.randint(0, max(total_items - 20, 0))

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q={query}"
            f"&startIndex={start_index}"
            f"&maxResults=20"
            f"&key={GOOGLE_BOOKS_API_KEY}"
        )

    items = []
    for attempt in range(18):
        response = requests.get(url).json()
        items = response.get("items", [])
        if items:
            break

    if not items:
        state["step"] = 2
        return "No books found for these categories."

    book = random.choice(items)
    volume_info = book.get("volumeInfo", {})
    
    global description, year, publisher, authors, title
    description = volume_info.get("description", "I do not have information about this book.")
    year = volume_info.get("publishedDate", "Year not available")[:4]
    publisher = volume_info.get("publisher", "Publisher not available")
    title = volume_info.get("title", "Unknown Title")
    authors = volume_info.get("authors", ["Unknown Author"])

    return f"Recommended Book: '{title}' by {', '.join(authors)} <br>{random.choice(describe_responses)}"


def recommend_book_three_categories(category1, category2, category3):
    category_id1 = CATEGORY_NAMES_BOOKS.get(category1)
    category_id2 = CATEGORY_NAMES_BOOKS.get(category2)
    category_id3 = CATEGORY_NAMES_BOOKS.get(category3)
    if not category_id1 or not category_id2 or not category_id3:
        state["step"] = 2
        return random.choice(invalid_responses)

    today = datetime.today()
    three_years_ago = today.replace(year=today.year - 3)

    query = f"subject:{category_id1}+subject:{category_id2}+subject:{category_id3}"

    if state["suggestion"] == "high":
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
        ).json()
        total_items = response.get("totalItems", 100)
        start_index = random.randint(0, max(total_items - 20, 0))

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q={query}"
            f"&startIndex={start_index}"
            f"&maxResults=20"
            f"&key={GOOGLE_BOOKS_API_KEY}"
        )

    elif state["suggestion"] == "new":
        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q={query}+publishedDate:{three_years_ago.strftime('%Y')}-{today.strftime('%Y')}"
            f"&maxResults=20"
            f"&orderBy=newest"
            f"&key={GOOGLE_BOOKS_API_KEY}"
        )
    elif state["suggestion"] == "bad":
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q=subject:{query}&key={GOOGLE_BOOKS_API_KEY}"
        ).json()
        total_items = response.get("totalItems", 100)
        start_index = random.randint(0, max(total_items - 20, 0))

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q=subject:{query}"
            f"&startIndex={start_index}"
            f"&maxResults=20"
            f"&key={GOOGLE_BOOKS_API_KEY}"
            f"&filter=free-ebooks"
        )
    else:
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_BOOKS_API_KEY}"
        ).json()
        total_items = response.get("totalItems", 100)
        start_index = random.randint(0, max(total_items - 20, 0))

        url = (
            f"https://www.googleapis.com/books/v1/volumes"
            f"?q={query}"
            f"&startIndex={start_index}"
            f"&maxResults=20"
            f"&key={GOOGLE_BOOKS_API_KEY}"
        )

    items = []
    for attempt in range(20):
        response = requests.get(url).json()
        items = response.get("items", [])
        if items:
            break

    if not items:
        state["step"] = 2
        return "No books found for these categories."

    book = random.choice(items)
    volume_info = book.get("volumeInfo", {})
    
    global description, year, publisher, authors, title
    description = volume_info.get("description", "I do not have information about this book.")
    year = volume_info.get("publishedDate", "Year not available")[:4]
    publisher = volume_info.get("publisher", "Publisher not available")
    title = volume_info.get("title", "Unknown Title")
    authors = volume_info.get("authors", ["Unknown Author"])

    return f"Recommended Book: '{title}' by {', '.join(authors)} <br>{random.choice(describe_responses)}"






# ----------------------------
# Bu function girilen metne göre film,dizi,kitap arasından hangisi veya hangileri hakkında konuşmak istendiğini tespit ediyor
# ----------------------------
def take_user_request(req):
  req = re.sub("[^a-zA-Z]"," ",req)
  req = req.lower()
  req = str(req)
  words = word_tokenize(req)
  words = [word for word in words if not word in set(stopwords.words("english"))]
  lematizer = nltk.WordNetLemmatizer()
  clean_words = []
  key_words = []
  for i in words:
    clean_words.append(lematizer.lemmatize(i))
  for i in clean_words:
    for key in konular:
      for j in konular[key]:
        if string_benzerlik(i,j):
          key_words.append(key)
  key_words = list(set(key_words))
  return key_words if key_words else ["BOŞ"]

# --------------------------------
# Bu fonksiyonlar girilen metindeki türleri tespit edip listeliyor
# --------------------------------

def take_movie_type(req):
  # Cümlede geçen film türlerini tespit edip listeler
  req = re.sub("[^a-zA-Z]"," ",req)
  req = req.lower()
  req = str(req)
  words = word_tokenize(req)
  words = [word for word in words if not word in set(stopwords.words("english"))]
  clean_words = []
  movie_types_collection = []
  for i in words:
    clean_words.append(i)
  for i in clean_words:
    for j in CATEGORY_NAMES_MOVIE:
      if string_benzerlik(i,j):
        movie_types_collection.append(j)
  movie_types_collection = list(set(movie_types_collection))
  if movie_types_collection:
      return movie_types_collection
  if test_movie_category_keyword(req):
      return test_movie_category_keyword(req)
  return detect_movie_category(req)

def take_serie_type(req):
  # Cümlede geçen dizi türlerini tespit edip listeler
  req = re.sub("[^a-zA-Z]"," ",req)
  req = req.lower()
  req = str(req)
  words = word_tokenize(req)
  words = [word for word in words if not word in set(stopwords.words("english"))]
  clean_words = []
  movie_types_collection = []
  for i in words:
    clean_words.append(i)
  for i in clean_words:
    for j in CATEGORY_NAMES_TV:
      if string_benzerlik(i,j):
        movie_types_collection.append(j)
  movie_types_collection = list(set(movie_types_collection))
  if movie_types_collection:
      return movie_types_collection
  if test_tv_category_keyword(req):
      return test_tv_category_keyword(req)
  return detect_tv_category(req)

def take_book_type(req):
  # Cümlede geçen kitap türlerini tespit edip listeler
  req = re.sub("[^a-zA-Z]"," ",req)
  req = req.lower()
  req = str(req)
  words = word_tokenize(req)
  words = [word for word in words if not word in set(stopwords.words("english"))]
  clean_words = []
  movie_types_collection = []
  for i in words:
    clean_words.append(i)
  for i in clean_words:
    for j in CATEGORY_NAMES_BOOKS:
      if string_benzerlik(i,j):
        movie_types_collection.append(j)
  movie_types_collection = list(set(movie_types_collection))
  if movie_types_collection:
      return movie_types_collection
  if test_book_category_keyword(req):
        return test_book_category_keyword(req)
  return detect_book_category(req)









def test_movie_category_keyword(test_string):
    matching_categories = []
    for category, keywords in movie_category_keywords.items():
        for keyword in keywords:
            if string_benzerlik(test_string, keyword):
                matching_categories.append(category)
                break
    return matching_categories

def test_tv_category_keyword(test_string):
    matching_categories = []
    for category, keywords in tv_category_keywords.items():
        for keyword in keywords:
            if string_benzerlik(test_string, keyword):
                matching_categories.append(category)
                break
    return matching_categories

def test_book_category_keyword(test_string):
    matching_categories = []
    for category, keywords in book_category_keywords.items():
        for keyword in keywords:
            if string_benzerlik(test_string, keyword):
                matching_categories.append(category)
                break
    return matching_categories








# --------------------------------
# Bu fonksiyon 3 tür arasından seçim yapıyor
# --------------------------------
def take_main_type(req):
    for i in take_user_request(req):
        if i == "movies":
            state["selection"] = "movies"
            return "What kind of movies you would like to watch?"
        elif i == "series":
            state["selection"] = "series"
            return "What kind of series you would like to watch?"
        elif i == "books":
            state["selection"] = "books"
            return "What kind of books you would like to read?"
        else:
            state["step"] = 1 
            return random.choice(clarification_responses)   
        
        

# --------------------------------
# Bu fonksiyon istenen kategorileri alıyor
# --------------------------------        
def make_recommendation(req):
    #bu fonksiyon new good bad belirleme işi >>>
    choose_content_characteristics(req)    
    # >>>
    if state["selection"] == "movies":
        if take_movie_type(req) == 0:
            return 0
        else:
            if len(take_movie_type(req)) == 1:
                return recommend_movie_one_category(take_movie_type(req)[0])
            elif len(take_movie_type(req)) == 2:
                return recommend_movie_two_categories(take_movie_type(req)[0], take_movie_type(req)[1])
            elif len(take_movie_type(req)) == 3:
                return recommend_movie_three_categories(take_movie_type(req)[0], take_movie_type(req)[1], take_movie_type(req)[2])
    elif state["selection"] == "series":
        if take_serie_type(req) == 0:
            return 0
        else:
            if len(take_serie_type(req)) == 1:
                return recommend_tv_one_category(take_serie_type(req)[0])
            elif len(take_serie_type(req)) == 2:
                return recommend_tv_two_categories(take_serie_type(req)[0], take_serie_type(req)[1])
            elif len(take_serie_type(req)) == 3:
                return recommend_tv_three_categories(take_serie_type(req)[0], take_serie_type(req)[1], take_serie_type(req)[2])
    elif state["selection"] == "books":
        if take_book_type(req) == 0:
            return 0
        else:
            if len(take_book_type(req)) == 1:
                return recommend_book_one_category(take_book_type(req)[0])
            elif len(take_book_type(req)) == 2:
                return recommend_book_two_categories(take_book_type(req)[0], take_book_type(req)[1])
            elif len(take_book_type(req)) == 3:
                return recommend_book_three_categories(take_book_type(req)[0], take_book_type(req)[1], take_book_type(req)[2])
    return 0
    
def start():
    return random.choice(start_responses)
def string_benzerlik(string1, string2):
    return SequenceMatcher(None, string1, string2).ratio() > 0.80
def greeting(req):
    for i in greetings_sentences:
        if string_benzerlik(i,req):
            return random.choice(greeting_responses)
def stop(req):
    for i in stop_sentences:
        if string_benzerlik(i,req):
            return random.choice(stop_responses)
def curse(req):
    for i in curse_sentences:
        if string_benzerlik(i,req):
            return random.choice(curse_responses)
def reset(req):      
    for i in reset_sentences:
        if string_benzerlik(i,req):
            return random.choice(reset_responses)   
def previous(req):
    for i in previous_sentences:
        if string_benzerlik(i,req):
            return random.choice(previous_responses)
def adult_content(req):
    for i in sexual_sentences:
        if string_benzerlik(i,req):
            return random.choice(sexual_content_responses)
        
        
        
def rejection_func(req):
    req = req.lower()
    for i in rejections:
        if string_benzerlik(i,req):
            return 1
def acceptance_func(req):
    req = req.lower()
    for i in acceptances:
        if string_benzerlik(i,req):
            return 1        
        

             
# bu ana fonksiyonda en son olacak 
def invalid_response():
    return random.choice(invalid_responses)
    
    
def unusual_response1(req):
    # step değişmez
    req = re.sub("[^a-zA-Z]"," ",req)
    req = req.lower()
    req = req.strip()
    
    adult1 = adult_content(req)
    if adult1:
        return adult1
    curse1 = curse(req)
    if curse1:
        return curse1
    previous1 = previous(req)
    if previous1:
        return previous1
        
        
def unusual_response2(req):
    # step 0 olur
    req = re.sub("[^a-zA-Z]"," ",req)
    req = req.lower()
    req = req.strip()    
    
    stop1 = stop(req)
    if stop1:
        return stop1
    reset1 = reset(req)
    if reset1:
        return reset1
    greet1 = greeting(req)
    if greet1:
        return greet1
    
    
    

def inform_user():
    if state["selection"] == "books":
        return f"Book: {title} <br>Year: {year}<br>Authors: {', '.join(authors)}<br>Publisher: {publisher}<br>"  + random.choice(describe_responses)
    return f"Name:{title} <br>Year: {year}<br>Director: {director}<br>Cast: {', '.join(cast)}<br>"  + random.choice(describe_responses)

def inform_user_more():
    return description + "<br><br>" + random.choice(resume_responses)


def accept_reject(req):
    labels = ["yes", "no"]
    result = classifier(req, labels)
    return 1 if result['labels'][0] == "yes" else 0


#********************************************************************************************************************
#********************************************************************************************************************
def detect_content_conditions(req):
    req_lower = req.lower()
    new_keywords = ["new", "recent", "latest", "fresh", "current", "modern","newest"]
    good_keywords = ["good", "great", "excellent", "awesome", "fantastic", "superb","high","quality","best","top","cool","nice","fine","wonderful","amazing","brilliant","fabulous","super","terrific","excellent","exceptional","outstanding","perfect","remarkable","stellar","superior","premium","deluxe","high-quality"]
    bad_keywords = ["bad", "poor", "terrible", "awful", "horrible", "subpar","low","worst","badly","poorly","terribly","awfully","horribly","subpar","inferior","low-quality","trash","garbage","junk","rubbish","crap","shitty","lousy","crappy","sucky","suck","sucks"]
    new_found = False
    good_found = False
    bad_found = False
    
    for kw in new_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', req_lower):
            new_found = True
            break
    for kw in good_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', req_lower):
            good_found = True
            break
    for kw in bad_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', req_lower):
            bad_found = True
            break
    return f"{int(new_found)}{int(good_found)}{int(bad_found)}"

def choose_content_characteristics(req):
    conditions = detect_content_conditions(req)
    if conditions == "100":
        state["suggestion"] = "new"
    elif conditions == "010":
        state["suggestion"] = "high"
    elif conditions == "001":
        state["suggestion"] = "bad"
    else:
        pass

#********************************************************************************************************************
#********************************************************************************************************************






def detect_movie_category(req):
    user_embedding = model111.encode(req)
    best_category = None
    best_similarity = 0
    for category, keywords in movie_category_keywords.items():
        keyword_embeddings = model111.encode(keywords)
        similarities = [util.cos_sim(user_embedding, keyword_emb).item() for keyword_emb in keyword_embeddings]
        max_similarity = max(similarities)
        if max_similarity > best_similarity:
            best_similarity = max_similarity
            best_category = category
    if best_similarity > 0.5:
        return CATEGORY_NAMES_MOVIE[best_category]
    return 0
def detect_tv_category(req):
    user_embedding = model111.encode(req)
    best_category = None
    best_similarity = 0
    for category, keywords in tv_category_keywords.items():
        keyword_embeddings = model111.encode(keywords)
        similarities = [util.cos_sim(user_embedding, keyword_emb).item() for keyword_emb in keyword_embeddings]
        max_similarity = max(similarities)
        if max_similarity > best_similarity:
            best_similarity = max_similarity
            best_category = category
    if best_similarity > 0.5:
        return CATEGORY_NAMES_TV[best_category]
    return False
def detect_book_category(req):
    user_embedding = model111.encode(req)
    best_category = None
    best_similarity = 0
    for category, keywords in book_category_keywords.items():
        keyword_embeddings = model111.encode(keywords)
        similarities = [util.cos_sim(user_embedding, keyword_emb).item() for keyword_emb in keyword_embeddings]
        max_similarity = max(similarities)
        if max_similarity > best_similarity:
            best_similarity = max_similarity
            best_category = category
    if best_similarity > 0.5:
        return CATEGORY_NAMES_BOOKS[best_category]
    return False


#****************************************************


def is_suggestion_request(req):
    threshold=0.7
    suggestion_keywords = {
        'suggest', 'recommend', 'advice', 'should', 'could',
        'option', 'choose', 'pick', 'between', 'alternatives',
        'idea', 'prefer', 'help', 'decide'
    }
    text_clean = re.sub(r'[^\w\s]', '', req.lower()).split()
    keyword_found = any(
        any(SequenceMatcher(None, word, kw).ratio() > 0.85 
            for kw in suggestion_keywords)
        for word in text_clean
    )
    if not keyword_found:
        return False  
    candidate_labels = ["suggestion request", "general inquiry"]
    result = classifier444(req, candidate_labels)
    suggestion_score = result['scores'][result['labels'].index("suggestion request")]
    return suggestion_score > (threshold * 0.9 if keyword_found else threshold * 1.1)

def chat_with_bot(req):
    global chat_history_ids
    if direct_suggestion(req) is not None:
        return direct_suggestion(req)
    elif is_suggestion_request(req):
        state["step"] = 1
        return start()
    else:
        tokenizer222.pad_token = tokenizer222.eos_token
        new_user_input_ids = tokenizer222.encode("This is a serious conversation. " + req + tokenizer222.eos_token, 
                                                 return_tensors='pt', max_length=512, truncation=True)

        if chat_history_ids is not None:
            bot_input_ids = torch.cat([chat_history_ids[:, -6:], new_user_input_ids], dim=-1)  # Son 6 mesajı tut
        else:
            bot_input_ids = new_user_input_ids

        attention_mask = torch.ones_like(bot_input_ids)
        chat_history_ids = model222.generate(
            bot_input_ids,
            attention_mask=attention_mask,
            max_new_tokens=128,
            pad_token_id=tokenizer222.eos_token_id,
            do_sample=True,
            temperature=0.3, 
            top_p=0.9, 
            repetition_penalty=1.2,
            no_repeat_ngram_size=2
        )

        response = tokenizer222.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True).strip()
        
        if len(response) < 3 or response in ["O", "E", "Woo", "Yay", "Ok"]:
            chat_history_ids = model222.generate(
                bot_input_ids,
                attention_mask=attention_mask,
                max_new_tokens=128,
                pad_token_id=tokenizer222.eos_token_id,
                do_sample=False,  
                temperature=0.4,
                top_p=0.85,
                repetition_penalty=1.3,
                no_repeat_ngram_size=3
            )
            response = tokenizer222.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True).strip()

        return response.capitalize()





#****************************************************
#Not : EĞER OLUR OLMADIK WHAT KİND OF MOVİES BOOKS GİBİ ŞEYLER GELİYORSA BURASI GEREĞİNDEN FAZLA TRUE DÖNÜYOR DEMEK 0.8 İ 85 VEYA 90 YAPABİLİRİZ BUNU DÜZELTMEK İÇİN 
def direct_suggestion(req):
    etiketler = [
        "asking for a movie recommendation", 
        "asking for a TV show recommendation", 
        "asking for a book recommendation", 
        "random statement"
    ]
    sonuc = classifier(req, candidate_labels=etiketler)
    etiket_skorlari = dict(zip(sonuc['labels'], sonuc['scores']))
    en_yuksek_etiket = max(etiket_skorlari, key=etiket_skorlari.get)

    if etiket_skorlari[en_yuksek_etiket] > 0.85:
        if en_yuksek_etiket == "asking for a movie recommendation":
            state["selection"] = "movies"
            state["step"] = 2
            return random.choice(ask_movie_type)
        elif en_yuksek_etiket == "asking for a TV show recommendation":
            state["selection"] = "series"
            state["step"] = 2
            return random.choice(ask_serie_type)
        elif en_yuksek_etiket == "asking for a book recommendation":
            state["selection"] = "books"
            state["step"] = 2
            return random.choice(ask_book_type)
    return None

   

#****************************************************
#kategori önerisi istiyor mu bunu tespit eden fonksiyon
def is_category(req):
    sentence_vectorized = vectorizer.transform([req])
    y_pred_proba = clf.predict_proba(sentence_vectorized)[:, 1]
    y_pred = (y_pred_proba > 0.8).astype(int)
    return bool(y_pred[0])

#****************************************************

def random_movie_categories():
    return random.sample(list(CATEGORY_NAMES_MOVIE.keys()), random.randint(3, 7))

def random_tv_categories():
    return random.sample(list(CATEGORY_NAMES_TV.keys()), random.randint(3, 7))

def random_book_categories():
    return random.sample(list(CATEGORY_NAMES_BOOKS.keys()), random.randint(3, 7))


def category_recommendations():
    movie_categories = random_movie_categories()
    tv_categories = random_tv_categories()
    book_categories = random_book_categories()
    if state["selection"] == "movies":
        return f"Movie Categories: {', '.join(movie_categories)}"
    elif state["selection"] == "series":
        return f"TV Show Categories: {', '.join(tv_categories)}"
    elif state["selection"] == "books": 
        return f"Book Categories: {', '.join(book_categories)}"
    

    
def send_to_step_N(req):
    if rejection_func(req) == 1:
        state["step"] = 0
        return random.choice(rejection_responses)
    if acceptance_func(req) == 1:
        state["step"] = 1
        return random.choice(start_responses_short)
    else:
        return chat_with_bot(req)
        

def send_to_step_M(req):  
    if direct_suggestion(req) != None:
        state["step"] = 2
        return direct_suggestion(req)
    else:
        return random.choice(clarification_responses)
  
  
def send_to_passive(req):  
    if direct_suggestion(req) != None:
        state["step"] = 2
        return direct_suggestion(req)
    return None

  
  
        
def recommend_RV(req):
    if state["step"] == 0:
        resp1 = unusual_response1(req)
        if resp1:
            return resp1
        resp2 = unusual_response2(req)
        if resp2:
            state["step"] = 0
            return resp2
        if send_to_passive(req) != None:
            return send_to_passive(req)
        else:
            state["step"] = 1
            return start()
    
    elif state["step"] == 1:
        resp1 = unusual_response1(req)
        if resp1:
            return resp1
        resp2 = unusual_response2(req)
        if resp2:
            state["step"] = 0
            return resp2
        if send_to_passive(req) != None:
            return send_to_passive(req)
        else:
            state["step"] = 2
            return take_main_type(req)
    
    elif state["step"] == 2:
        resp1 = unusual_response1(req)
        if resp1:
            return resp1
        resp2 = unusual_response2(req)
        if resp2:
            state["step"] = 0
            return resp2
        if make_recommendation(req) != 0:
            state["step"] = 3
            return make_recommendation(req)
        if is_category(req) == True:
            return category_recommendations()
        else:
            return random.choice(clarification_responses)
        
    elif state["step"] == 3:
        resp1 = unusual_response1(req)
        if resp1:
            return resp1
        resp2 = unusual_response2(req)
        if resp2:
            state["step"] = 0
            return resp2
        if accept_reject(req) == 1:
            state["step"] = 4
            return inform_user()
        else:
            return send_to_step_N(req)
        
    elif state["step"] == 4:
        resp1 = unusual_response1(req)
        if resp1:
            return resp1
        resp2 = unusual_response2(req)
        if resp2:
            state["step"] = 0
            return resp2
        if accept_reject(req) == 1:
            state["step"] = 5
            return inform_user_more()
        else:
            return send_to_step_N(req)
    elif state["step"] == 5:
        resp1 = unusual_response1(req)
        if resp1:
            return resp1
        resp2 = unusual_response2(req)
        if resp2:
            state["step"] = 0
            return resp2
        return send_to_step_N(req)
    elif state["step"] == 6:
        resp1 = unusual_response1(req)
        if resp1:
            return resp1
        resp2 = unusual_response2(req)
        if resp2:
            state["step"] = 0
            return resp2
        return chat_with_bot(req)    
    else: 
        return "Unknown Step"
    