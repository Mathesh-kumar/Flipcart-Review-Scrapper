"""
    FLIPCART PRODUCT REVIEW SCRAPPING
    (i.e, Product name, feature, description, reviews and ratings)
"""

# Import needed libraries
from flask import Flask, request, render_template  # Light weight WSGI web application framework
from bs4 import BeautifulSoup  # Makes easy to scrap contents from web page
import requests  # Simple, elegant HTTP library
import mongodbServer
import productDetails

app = Flask(__name__)  # Flask app initialization

def get_page(url):
    page = requests.get(url)  # Request webpage from internet
    productPage = BeautifulSoup(page.text, "html.parser")  # Parse web page as html
    return productPage


"""
Function to scrap reviews of a specified product from the flipcart page
"""
@app.route('/', methods=['POST', 'GET'])  # Route with POST & GET methods
def review_scrapping():  # Function to scrap contents
    if request.method == 'POST':  # If method==POST, scrap contents from flipcart page & display
        productName = request.form['content'].replace(" ", "")  # Product name to search

        try:
            reviewsFromServer = mongodbServer.search_collection(productName)
            if len(reviewsFromServer) > 0:  # If the review count >0 show output to the user
                return render_template('results.html', reviews=reviewsFromServer)  # Show product reviews to the user
            else:  # else search in flipcart site
                reviewsToServer = []

                productURL = "https://www.flipkart.com/search?q=" + productName  # URL to search on flipcart
                mainProductPage = get_page(productURL)
                allProducts = mainProductPage.findAll("div", {"class": "_13oc-S"})  # Select all products

                for i in range(len(allProducts)):
                    firstProduct = allProducts[i]  # Select first product from the list of products
                    uniqueProductLink = "https://www.flipkart.com" + firstProduct.div.div.a['href']  # Select first product link
                    uniqueProductPage = get_page(uniqueProductLink)
                    reviewList = productDetails.get_details(uniqueProductLink, uniqueProductPage)
                    reviewsToServer.append(reviewList)  # Append each review as dictionary into reviews list

                mongodbServer.create_collection(productName, reviewsToServer[:20])

                try:
                    return render_template('results.html', reviews=reviewsToServer)  # Show product reviews to the user
                except:
                    return "Scrapping success HTML page error"
        except:
            return "OOPS! Something gone wrong, Try some different product"
    else:  # If method==GET, show the index page to type product name
        return render_template('index.html')  # Show search bar page to the user


if __name__ == '__main__':  # Starting point of program - main function
    app.run(debug=True)  # Run app on local host