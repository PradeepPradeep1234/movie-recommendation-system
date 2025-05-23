import pandas as pd
import requests
import urllib.parse
import time
import asyncio
import aiohttp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = '0a7a42d3e393653ba495817fab7e4201'  # Replace with your real TMDB API key

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
}

def safe_get(url, retries=3, delay=2, timeout=5):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == retries - 1:
                print(f"Request failed after {retries} attempts: {e}")
                return None
            time.sleep(delay)

# Load and prepare dataset
movies = pd.read_csv('dataset/movies.csv')
movies['combined'] = movies['genres'].fillna('') + ' ' + movies['keywords'].fillna('') + ' ' + movies['overview'].fillna('')

vectorizer = TfidfVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(movies['combined'])


def search_movie_tmdb(query):
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={encoded_query}"
    response = safe_get(url)
    if not response:
        return None
    results = response.json().get('results')
    if results:
        return results[0]
    return None


def get_movie_metadata(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US&append_to_response=keywords"
    response = safe_get(url)
    if not response:
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


async def fetch(session, url):
    async with session.get(url, headers=HEADERS) as response:
        response.raise_for_status()
        return await response.json()


async def get_movie_details_async(movie_ids):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for movie_id in movie_ids:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
            tasks.append(fetch(session, url))
        results = await asyncio.gather(*tasks, return_exceptions=True)

    details = []
    for data in results:
        if isinstance(data, Exception):
            continue
        details.append({
            'title': data.get('title'),
            'overview': data.get('overview'),
            'poster': f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}" if data.get('poster_path') else '',
            'rating': data.get('vote_average'),
            'link': f"https://www.themoviedb.org/movie/{data.get('id')}"
        })
    return details


def recommend_dynamic(movie_name):
    movie = search_movie_tmdb(movie_name)
    if not movie:
        return []

    metadata = get_movie_metadata(movie['id'])
    if not metadata:
        return []

    similar = recommend_from_text(metadata)

    # Limit to top 5 movies for async details fetch
    movie_ids = similar['id'].tolist()[:5]
    recommendations = asyncio.run(get_movie_details_async(movie_ids))

    return recommendations
