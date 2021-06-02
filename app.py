"""
    FLIPCART PRODUCT REVIEW SCRAPPING
    (i.e, Product name, feature, description, reviews and ratings)
"""

# Import needed libraries
from flask import Flask, jsonify  # Light weight WSGI web application framework
from bs4 import BeautifulSoup  # Makes easy to scrap contents from web page
import requests  # Simple, elegant HTTP library
import mongodbServer
import productDetails

cache = {}
app = Flask(__name__)  # Flask app initialization

def get_page(url):
    page = requests.get(url)  # Request webpage from internet
    productPage = BeautifulSoup(page.text, "html.parser")  # Parse web page as html
    return productPage


"""
Function to scrap reviews of a specified product from the flipcart page
"""
@app.route('/search/<product>', methods=['GET'])  # Route with POST & GET methods
def review_scrapping(product):  # Function to scrap contents
    productName = product  # Product name to search

    try:
        reviewsFromServer = mongodbServer.search_collection(productName)
        if len(reviewsFromServer) > 0:  # If the review count >0 show output to the user
            try:
                cache['result'] = reviewsFromServer
                return jsonify(reviewsFromServer)  # Show product reviews to the user
            except:
                error = {"mess": "OPPS!! Something went wrong during collection retrival"}
                return jsonify(error)
        else:  # else search in flipcart site
            reviewsToServer = []

            productURL = "https://www.flipkart.com/search?q=" + productName  # URL to search on flipcart
            mainProductPage = get_page(productURL)
            allProducts = mainProductPage.findAll("div", {"class": "_13oc-S"})  # Select all products

            allProducts = allProducts[:8]
            for i in range(len(allProducts)):
                firstProduct = allProducts[i]  # Select first product from the list of products
                uniqueProductLink = "https://www.flipkart.com" + firstProduct.div.div.a['href']  # Select first product link
                uniqueProductPage = get_page(uniqueProductLink)
                reviewList = productDetails.get_details(uniqueProductLink, uniqueProductPage)
                reviewsToServer.append(reviewList)  # Append each review as dictionary into reviews list

            mongodbServer.create_collection(productName, reviewsToServer)

            reviewsToServer = mongodbServer.search_collection(productName)
            cache['result'] = reviewsToServer
            try:
                return jsonify(reviewsToServer)  # Show product reviews to the user
            except:
                error = {"mess": "OPPS!! Something went wrong during collection updation."}
                return jsonify(error)
    except:
        error = {"mess": "OPPS!! Product not found , Try different product.."}
        return jsonify(error)


@app.route('/product/<pid>', methods=['GET'])
def display_product_reviews(pid):
    return jsonify(cache['result'][pid])


if __name__ == '__main__':  # Starting point of program - main function
    app.run(debug=True)  # Run app on local host