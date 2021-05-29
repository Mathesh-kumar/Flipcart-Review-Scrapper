"""
This is used to connect with mongodb atlas server
To perform operations such as search collection and create new collection
"""

import pymongo  # Contains tools for interacting with MongoDB database from Python

def credential():
    (USER_NAME, PASSWORD, DB_NAME) = ("root", "root", "flipcart")  # Credentials for mongodb atlas connection with database name
    CONNECTION_URL = f"mongodb+srv://{USER_NAME}:{PASSWORD}@flipcartreview.t8qf3.mongodb.net/{DB_NAME}?ssl=true&ssl_cert_reqs=CERT_NONE"
    client = pymongo.MongoClient(CONNECTION_URL)  # Establish connection with mongodb server
    dataBase = client[DB_NAME]  # Create DB / Use existing database
    return dataBase

def search_collection(product):
    dataBase = credential()
    flipcartReviews = dataBase[product].find({}, {'_id': 0})  # Search whether product reviews already present in the database

    reviews = []  # List to store the comments
    for review in enumerate(flipcartReviews):  # Iterate through each review. Since flipcartReviews is an mongodb cursor object
        reviews.append(review[1])  # Append each review to the reviews list
    return reviews

def create_collection(product, reviews):
    dataBase = credential()
    collection = dataBase[product]  # Create a collection
    collection.insert_many(reviews)  # Insert all the reviews into the collection