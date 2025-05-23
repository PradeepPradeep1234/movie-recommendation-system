import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = '0a7a42d3e393653ba495817fab7e4201'  # 🔁 Replace with your real TMDB API key

# Load and prepare dataset
movies = pd.read_csv('dataset/movies.csv')
movies['combined'] = movies['genres'] + ' ' + movies['keywords'] + ' ' + movies['overview']
movies['combined'] = movies['combined'].fillna('')


vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(movies['combined'])


def search_movie_tmdb(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
    response = requests.get(url)
    results = response.json().get('results')
    if results:
        return results[0]  # Return best match
    return None


def get_movie_metadata(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US&append_to_response=keywords"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()

    genres = ' '.join([g['name'] for g in data.get('genres', [])])
    keywords = ' '.join([kw['name'] for kw in data.get('keywords', {}).get('keywords', [])])
    overview = data.get('overview', '')

    return genres + ' ' + keywords + ' ' + overview


def recommend_from_text(text):
    input_vec = vectorizer.transform([text])
    similarity = cosine_similarity(input_vec, vectors)
    top_indices = similarity[0].argsort()[-10:][::-1]
    return movies.iloc[top_indices][['title', 'id']]


def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return {
        'title': data.get('title'),
        'overview': data.get('overview'),
        'poster': f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get('poster_path') else '',
        'rating': data.get('vote_average'),
        'link': f"https://www.themoviedb.org/movie/{data.get('id')}"
    }


def recommend_dynamic(movie_name):
    movie = search_movie_tmdb(movie_name)
    if not movie:
        return []

    metadata = get_movie_metadata(movie['id'])
    if not metadata:
        return []

    similar = recommend_from_text(metadata)
    recommendations = []

    for _, row in similar.iterrows():
        details = get_movie_details(row['id'])
        if details:
            recommendations.append(details)

    return recommendations
