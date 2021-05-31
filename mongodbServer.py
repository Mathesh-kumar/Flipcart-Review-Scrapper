# Import needed libraries

import pymongo  # Contains tools for interacting with MongoDB database from Python


"""
    Function to create connection to the mongo atlas server
    Returns database connection.
"""
def credential():
    (USER_NAME, PASSWORD, DB_NAME) = ("root", "root", "flipcart")  # Credentials for mongodb atlas connection with database name
    CONNECTION_URL = f"mongodb+srv://{USER_NAME}:{PASSWORD}@flipcartreview.t8qf3.mongodb.net/{DB_NAME}?ssl=true&ssl_cert_reqs=CERT_NONE"
    client = pymongo.MongoClient(CONNECTION_URL)  # Establish connection with mongodb server
    dataBase = client[DB_NAME]  # Create DB / Use existing database
    return dataBase


"""
    Function to search for a specific collection in the database.
    Requires one argument (i.e, product name)
    Returns list of product details if the product found in the database.
"""
def search_collection(product):
    dataBase = credential()  # Create connection to the database in mongo atlas server
    flipcartReviews = dataBase[product].find({})  # Search whether product reviews already present in the database

    # reviews = []  # List to store the comments
    # for review in enumerate(flipcartReviews):  # Iterate through each review. Since flipcartReviews is an mongodb cursor object
    #     pid = review[1]['_id']
    #     reviews.append({str(pid): review[1]['product']})
    # return reviews

    reviewList = {}

    for review in enumerate(flipcartReviews):
        pid = review[1]['_id']
        reviewList[str(pid)] = review[1]['product']
    return reviewList

"""
    Function to create new collection for the product searched in the database.
    Requires two arguments product name and product details(reviews).
"""
def create_collection(product, reviews):
    dataBase = credential() # Create connection to the database in mongo atlas server
    collection = dataBase[product]  # Create a collection
    collection.insert_many(reviews)  # Insert all the reviews into the collection