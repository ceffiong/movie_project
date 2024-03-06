from flask import Flask, render_template, request, redirect
import random
import statistics

app = Flask(__name__)

MOVIES = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "rating": 5,
        "image": "https://cdn.pixabay.com/photo/2017/08/10/00/52/house-2616607_1280.jpg"
    },
    {
        "id": 2,
        "title": "Pulp Fiction",
        "rating": 1,
        "image": "https://cdn.pixabay.com/photo/2017/11/24/05/38/jet-2974131_1280.jpg"
    },
    {
        "id": 3,
        "title": "The Room",
        "rating": 2,
        "image": "https://cdn.pixabay.com/photo/2018/10/26/11/14/man-3774381_1280.jpg"
    },
    {
        "id": 4,
        "title": "The Godfather",
        "rating": 5,
        "image": "https://cdn.pixabay.com/photo/2016/09/22/13/51/bollywood-1687410_1280.jpg"
    },
    {
        "id": 5,
        "title": "The Godfather: Part II",
        "rating": 4,
        "image": "https://cdn.pixabay.com/photo/2017/09/16/01/31/charlie-chaplin-2754312_1280.jpg"
    },
    {
        "id": 6,
        "title": "The Dark Knight",
        "rating": 3,
        "image": "https://cdn.pixabay.com/photo/2015/09/25/18/47/tunnel-957963_1280.jpg"
    },
    {
        "id": 7,
        "title": "Everything Everywhere All At Once",
        "rating": 3,
        "image": "https://cdn.pixabay.com/photo/2016/03/27/07/38/police-1282330_1280.jpg"
    },
    {
        "id": 8,
        "title": "12 Angry Men",
        "rating": 3,
        "image": "https://cdn.pixabay.com/photo/2015/09/03/17/28/man-921004_1280.jpg"
    },
    {
        "id": 9,
        "title": "Forrest Gump",
        "rating": 2,
        "image": "https://cdn.pixabay.com/photo/2018/02/13/23/41/nature-3151869_1280.jpg"
    },
    {
        "id": 10,
        "title": "Star Wars: Episode V",
        "rating": 4,
        "image": "https://cdn.pixabay.com/photo/2014/10/02/06/34/war-469503_1280.jpg"
    },
]

@app.route("/")
def index():
    # return first 4 movies
    movies = []
    for i in range(4):
        movies.append(MOVIES[i])

    return render_template('index.html', movies = movies)


@app.route("/movies", methods =["GET"])
def movie():
    return render_template('movie.html', movies = MOVIES)
        

@app.route("/movies/search", methods =["POST"])
def search_movies():
    title = request.form['title']
    if title:
        movies = []
        for movie in MOVIES:
            if title.lower() in movie["title"].lower():
                movies.append(movie)
        return render_template("movie.html", movies=movies)
    else:
        return redirect("/movies")

@app.route("/movies/random")
def random_movie():
    i = random.randint(0, 9)
    movie = MOVIES[i]
    print(movie)
    return render_template('random.html', movie = movie, title="Tonight's movie")

@app.route("/movies/sort")
def sort_movies():
    movies = sorted(MOVIES, key=lambda d: d['rating'], reverse=True)
    return render_template('movie.html', movies = movies, sort_desc="sort")

@app.route("/movies/stats")
def movies_stats():
    movies = sorted(MOVIES, key=lambda d: d['rating'], reverse=True)

    # Get all the ratings
    ratings = []
    for movie in movies:
        ratings.append(movie["rating"])
    
    average_rating = format(statistics.mean(ratings), '.2f')
    median_rating = format(statistics.median(ratings), '.2f')
    return render_template('stats.html', best_movie=movies[0], worst_movie=movies[-1], average_rating = average_rating, median_rating = median_rating)


@app.route("/movies/delete/<int:id>")
def delete(id):
    for i in range(len(MOVIES)):
        if id == MOVIES[i].get("id"):
            del MOVIES[i]
            break
    return render_template('movie.html', movies = MOVIES)


@app.route("/movies/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "GET":
        return render_template("movie.html", add_form="add_form", movies=MOVIES)
    else:
        # Get new movie details
        title = request.form['title']
        image = request.form['image']
        rating = int(request.form['rating'])

        movie = {
            "id": len(MOVIES) + 1,
            "title": title, 
            "image": image,
            "rating": rating
        }


        MOVIES.insert(0, movie)
        return redirect("/movies")

@app.route("/movies/edit/<int:id>", methods=['GET', 'POST'])
def edit_form(id):
    if request.method == "GET":
        # Find the movie data
        movie = {}
        for i in range(len(MOVIES)):
            if id == MOVIES[i].get("id"):
                movie = MOVIES[i]
                break
        return render_template('movie.html', movies = MOVIES, movie = movie)
    else:
        title = request.form['title']
        image = request.form['image']
        rating = int(request.form['rating'])

        # find the movie and update the values
        for i in range(len(MOVIES)):
            if id == MOVIES[i].get("id"):
                MOVIES[i]["title"] = title
                MOVIES[i]["image"] = image
                MOVIES[i]["rating"] = rating
                break
        return redirect("/movies")

if __name__ == "__main__":
    app.run(port=8000, debug=True)