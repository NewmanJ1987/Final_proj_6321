from pymongo import MongoClient

# Default  MongoDb Port
client = MongoClient('localhost:27017')
db = client.movies


# Query to retrieve all possible genres.
def get_all_genres_of_movies():
    return db.movies.distinct("genre")



# print(get_all_genres_of_movies())