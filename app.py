from flask import Flask, render_template, request, redirect
import random
import statistics
import os
import json

app = Flask(__name__)

def read_file(path=os.path.abspath("movies.json")):
    with open(path, "r") as f:
        data = json.load(f)
    return data

def write_file(data, path=os.path.abspath("movies.json")):
    json_str = json.dumps(data)
    with open(path, "w") as f: 
        f.write(json_str)

@app.route("/")
def index():
    # return first 4 movie
    movies = read_file(os.path.abspath("movies.json"))
    for i in range(4):
        movies.append(movies[i])

    return render_template('index.html', movies = movies)


@app.route("/movies", methods =["GET"])
def movie():
    movies = read_file(os.path.abspath("movies.json"))
    return render_template('movie.html', movies = movies)
        

@app.route("/movies/search", methods =["POST"])
def search_movies():
    title = request.form['title']
    if title:
        movies = read_file(os.path.abspath("movies.json"))
        for movie in movies:
            if title.lower() in movie["title"].lower():
                movies.append(movie)
        return render_template("movie.html", movies=movies)
    else:
        return redirect("/movies")

@app.route("/movies/random")
def random_movie():
    i = random.randint(0, 9)
    movies = read_file(os.path.abspath("movies.json"))
    movie = movies[i]
    print(movie)
    return render_template('random.html', movie = movie, title="Tonight's movie")

@app.route("/movies/sort")
def sort_movies():
    movies = read_file(os.path.abspath("movies.json"))
    movies = sorted(movies, key=lambda d: d['rating'], reverse=True)
    return render_template('movie.html', movies = movies, sort_desc="sort")

@app.route("/movies/stats")
def movies_stats():
    movies = read_file(os.path.abspath("movies.json"))
    movies = sorted(movies, key=lambda d: d['rating'], reverse=True)

    # Get all the ratings
    ratings = []
    for movie in movies:
        ratings.append(movie["rating"])
    
    average_rating = format(statistics.mean(ratings), '.2f')
    median_rating = format(statistics.median(ratings), '.2f')
    return render_template('stats.html', best_movie=movies[0], worst_movie=movies[-1], average_rating = average_rating, median_rating = median_rating)


@app.route("/movies/delete/<int:id>")
def delete(id):
    movies = read_file(os.path.abspath("movies.json"))
    for i in range(len(movies)):
        if id == movies[i].get("id"):
            del movies[i]
            break
    return render_template('movie.html', movies = movies)


@app.route("/movies/add", methods=["GET", "POST"])
def add_movie():
    if request.method == "GET":
        movies = read_file(os.path.abspath("movies.json"))
        return render_template("movie.html", add_form="add_form", movies=movies)
    else:
        movies = read_file(os.path.abspath("movies.json"))
        
        # Get new movie details
        title = request.form['title']
        image = request.form['image']
        rating = int(request.form['rating'])

        movie = {
            "id": len(movies) + 1,
            "title": title, 
            "image": image,
            "rating": rating
        }

        if title != "" and image != "" and rating != "":
            movies.insert(0, movie)

            # save the file
            write_file(movies, os.path.abspath("movies.json"))

        return redirect("/movies")




@app.route("/movies/edit/<int:id>", methods=['GET', 'POST'])
def edit_form(id):
    if request.method == "GET":
        movies = read_file(os.path.abspath("movies.json"))

        # Find the movie data
        movie = {}
        for i in range(len(movies)):
            if id == movies[i].get("id"):
                movie = movies[i]
                break
        return render_template('movie.html', movies = movies, movie = movie)
    else:
        movies = read_file(os.path.abspath("movies.json"))

        title = request.form['title']
        image = request.form['image']
        rating = int(request.form['rating'])

        # find the movie and update the values
        for i in range(len(movies)):
            if id == movies[i].get("id"):
                movies[i]["title"] = title
                movies[i]["image"] = image
                movies[i]["rating"] = rating
                
                # save the updates
                write_file(movies, os.path.abspath("movies.json"))
        return redirect("/movies")

if __name__ == "__main__":
    app.run(port=8000, debug=True)