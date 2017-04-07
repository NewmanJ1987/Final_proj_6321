import csv
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

client = MongoClient('localhost:27017')
db = client.movies




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
print "".join("-" for _ in range(80))
