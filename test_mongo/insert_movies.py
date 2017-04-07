import csv
from pymongo import MongoClient

# Default  MongoDb Port
client = MongoClient('localhost:27017')
db = client.movies


def read_insert_movies_from_csv():
    # You will need to update this with where you keep the csv file
    with open("/home/newman/PycharmProjects/movie_recos/ml-latest-small/movies.csv") as movies:
        movies_reader = csv.reader(movies)
        to_insert = [
            {
                "movie_id": movie[0],
                "_id": movie[0],
                "title": movie[1],
                "genre": movie[2].split("|")
            }
            for movie in movies_reader if movies_reader.line_num != 1
            ]
        db.movies.insert_many(to_insert)


read_insert_movies_from_csv()