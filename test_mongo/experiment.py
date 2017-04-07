from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

# Default  MongoDb Port
client = MongoClient('localhost:27017')
db = client.movies

user_ids = ["547", "564", "457", "23", "651", "604"]
for user_id in user_ids :
    features = list(db.ratings.find({"user_id": user_id}))
    inputs = [feature.get("genre_info") for feature in features]
    outputs = [feature.get("recommend") for feature in features]

    inputs_train, inputs_test, outputs_train, outputs_test = train_test_split(inputs, outputs, test_size=0.20)

    classifier = GaussianNB()
    classifier.fit(inputs_train, outputs_train)

    misclassification = 0
    total = 0
    for index in range(len(inputs_test)):
        prediction = classifier.predict(inputs_test[index])
        total += 1
        if prediction != outputs_test[index]:
            misclassification += 1

    print "Result for user id ", user_id,"."
    print "Number of misclassification [", misclassification, "] samples in test [", total, "] error percentage [", round(
        misclassification * 1.0 / total, 3), "]. "
    print "".join("-" for _ in range(86))
