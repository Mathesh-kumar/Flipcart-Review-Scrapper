# Flipcart product review scrapping - python code file

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

        # try:
        try:
            reviewsFromServer = mongodbServer.search_collection(productName)
        except:
            return "Error in mongodb collection search"

        if len(reviewsFromServer) > 0:  # If the review count >0 show output to the user
            return render_template('results.html', reviews=reviewsFromServer)  # Show product reviews to the user
        else:  # else search in flipcart site
            reviewsToServer = []

            try:
                productURL = "https://www.flipkart.com/search?q=" + productName  # URL to search on flipcart
                mainProductPage = get_page(productURL)
                allProducts = mainProductPage.findAll("div", {"class": "_13oc-S"})  # Select all products
            except:
                return "Error in opening product page"

            try:
                for i in range(len(allProducts)):
                    firstProduct = allProducts[i]  # Select first product from the list of products
                    firstProductLink = "https://www.flipkart.com" + firstProduct.div.div.a['href']  # Select first product link
                    uniqueProductPage = get_page(firstProductLink)
                    reviewList = productDetails.get_details(uniqueProductPage)
                    reviewsToServer.append(reviewList)  # Append each review as dictionary into reviews list
            except:
                return "Error in opening individual products"

            try:
                mongodbServer.create_collection(productName, reviewsToServer[:15])
            except:
                return "Error in mongodb collection creation"

            reviewsToServer = reviewsToServer

            try:
                return render_template('results.html', reviews=reviewsToServer)  # Show product reviews to the user
            except:
                return "After insertion to atlas display page error"
        # except:
        #    return "Something went wrong"
    else:  # If method==GET, show the index page to type product name
        return render_template('index.html')  # Show search bar page to the user


if __name__ == '__main__':  # Starting point of program - main function
    app.run(debug=True)  # Run app on local host