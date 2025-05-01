from flask import Flask, render_template, request
from recommendation import recommend_dynamic

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    movies = []
    if request.method == 'POST':
        movie_name = request.form['movie']
        movies = recommend_dynamic(movie_name)
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
