import csv
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

client = MongoClient('localhost:27017')
db = client.movies


def read_insert_movies_from_csv():
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


def read_insert_ratings_from_csv():
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


def add_recommend_based_on_ratings():
    for rating in db.ratings.find():
        if rating.get("rating") >= 2.5:
            db.ratings.update({"_id": rating.get("_id")}, {"$set": {"recommend": 1}}, False,
                              True)
        else:
            db.ratings.update({"_id": rating.get("_id")}, {"$set": {"recommend": 0}}, False,
                              True)


genres = ["Musical", "IMAX", "Documentary", "Sci-Fi", "Mystery", "Horror", "Comedy", "Children", "War", "Animation",
          "Adventure", "Fantasy", "Romance", "Crime", "(no genres listed)", "Film-Noir", "Western", "Action", "Drama",
          "Thriller"]

# ratings = list(db.ratings.find())
# inputs = [rating.get("genre_info") for rating in ratings]
# outputs = [rating.get("recommend") for rating in ratings]
#
# print(len(inputs))
# print(len(outputs))
#
# inputs_train, inputs_test, outputs_train, outputs_test = train_test_split(inputs, outputs, test_size=0.1)
#
# classifier = GaussianNB()
# classifier.fit(inputs_train, outputs_train)
#
# misclassification = 0
# total = 0
# for index in range(len(inputs_test)):
#     prediction = classifier.predict(inputs_test[index])
#     total += 1
#     if prediction != outputs_test[index]:
#         misclassification += 1
#
# # 24 percent misclassification with bayes just using genre.
# print "Number of misclassification [", misclassification, "] percentage [", misclassification * 1.0 / total, "] "



# Result for 651 65191

ratings_651 = list(db.ratings.find({"user_id": "651"}))
inputs = [rating.get("genre_info") for rating in ratings_651]
outputs = [rating.get("recommend") for rating in ratings_651]

print(len(inputs))
print(len(outputs))

inputs_train, inputs_test, outputs_train, outputs_test = train_test_split(inputs, outputs, test_size=0.05)

classifier = GaussianNB()
classifier.fit(inputs_train, outputs_train)

misclassification = 0
total = 0
for index in range(len(inputs_test)):
    prediction = classifier.predict(inputs_test[index])
    total += 1
    if prediction != outputs_test[index]:
        misclassification += 1

print "Result for user id 651."
print "Number of misclassification [", misclassification, "] samples in test [", total, "] percentage [", round(misclassification * 1.0 / total,3), "] "
