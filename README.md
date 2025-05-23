# 🎬 Movie Recommendation System



This is a content-based Movie Recommendation System built using **Flask**, **Pandas**, **Scikit-learn**, and the **TMDB API**. Users can enter any movie name, and the app recommends similar movies with posters, ratings, and brief overviews.

Dataset Link : https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata


🔗 **Live Demo**: [Click here to try the app](https://movie-recommendation-system-v243.onrender.com)

## API_KEY 

✅ Steps to Get TMDb API Key:

Go to TMDb Website:
Visit https://www.themoviedb.org

Create an Account:
Click on "Sign Up" and create a free account (or log in if you already have one).

Verify Your Email:
TMDb will send you a verification email. Click the link to verify your account.

Navigate to API Section:
After logging in, go to your profile > Settings > API or directly visit https://www.themoviedb.org/settings/api

Apply for an API Key:
Scroll down to "API Key" section. Choose "Developer" for personal projects.

Fill the Application Form:
Provide a brief name and description of your project. (e.g., “Personal Movie Recommender”)

Submit and Copy Your Key:
After approval, you’ll see your API key. Copy it and paste it into your code where needed.

---

## 🚀 Features

- 🔍 Search for a movie using TMDB
- 🎯 Get top 10 similar movies based on genres, keywords, and storyline
- 🖼️ View movie poster, rating, overview, and external link to TMDB
- 🌐 Live web interface built with Flask and Bootstrap

---

## 📝 Credits
- TMDB API  
- Bootstrap for UI

---

## How It Works

1. **Data Preparation**: The movie dataset is processed by combining genres, keywords, and overview into a single feature.
2. **Vectorization**: TF-IDF is used to convert text data into vectors.
3. **Similarity Matching**: Cosine similarity is computed to find movies most similar to the queried one.
4. **Dynamic TMDB API Calls**: When a user searches for a movie, the TMDB API fetches live data to enrich recommendations.

---

## 🧪 Example

1. Search: `Inception`
2. Output: Recommended movies like *Interstellar*, *The Prestige*, *Shutter Island*, etc. with posters and descriptions.

---

## 🛠️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/PradeepPradeep1234/movie-recommendation-system.git
cd movie-recommendation-system
pip install -r requirements.txt
