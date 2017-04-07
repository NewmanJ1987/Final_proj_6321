import csv
from queries import get_all_genres_of_movies
from pymongo import MongoClient

# Default  MongoDb Port
client = MongoClient('localhost:27017')
db = client.movies

genres = get_all_genres_of_movies()


def read_insert_ratings_from_csv():
    # You will need to update this with where you keep the csv file
    with open("/home/newman/PycharmProjects/movie_recos/ml-latest-small/ratings.csv") as ratings:
        ratings_reader = csv.reader(ratings)
        to_insert = []
        iter_reader = iter(ratings_reader)
        next(iter_reader)
        for rating in iter_reader:
            genre_info, title = retrieve_movie_genres_title(rating[1])
            to_insert.append({
                "user_id": rating[0],
                "genre_info": genre_info,
                "title": title,
                "movie_id": rating[1],
                "rating": float(rating[2]),
                "reccomend": 1 if float(rating[2]) >= 2.5 else 0,
                "time_stamp": rating[3]
            })
        db.ratings.insert_many(to_insert)


def retrieve_movie_genres_title(movie_id):
    genres_empty = [0 for _ in range(20)]
    movie = list(db.movies.find({"_id": movie_id}))[0]
    retrieved_genres = movie.get("genre")
    for genre in retrieved_genres:
        genres_empty[genres.index(genre)] = 1
    return genres_empty, movie.get("title")


read_insert_ratings_from_csv()
