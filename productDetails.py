# Import needed libraries
import requests
from bs4 import BeautifulSoup

"""
    Function to scrap product name from the flipcart page
    Requires one argument (i.e, source code of the page)
    Returns product name as string
"""
def get_product_name(page):
    try:
        prodName = page.find_all("h1", {"class": "yhB1nd"})[0].text  # Name of the product
    except:
        prodName = "No Name"
    return prodName


"""
    Function to scrap product sample image url from the flipcart page
    Requires one argument (i.e, source code of the page)
    Returns image url as string
"""
def get_product_image(page):
    try:
        imageLink = page.find_all("div", {"class": "CXW8mj _3nMexc"})[0].img['src']  # Sample image link of the product
    except:
        imageLink = "No Link"
    return imageLink


"""
    Function to scrap product highlights from the flipcart page
    Requires one argument (i.e, source code of the page)
    Returns product highlights as list of dictionary
"""
def get_product_highlights(page):
    try:
        prodHighs = {}
        highlights = page.find_all("li", {"class": "_21Ahn-"})  # Highlights of the product
        for i in range(len(highlights)):
            prodHighs[str(i)] = highlights[i].text
    except:
        prodHighs = {'0': "No highlights"}
    return [prodHighs]


"""
    Function to scrap product description from the flipcart page
    Requires one argument (i.e, source code of the page)
    Returns product description as string
"""
def get_product_description(page):
    try:
        prodDesc = page.find_all("div", {"class": "_1mXcCf RmoJUa"})[0].text  # Description about the product
    except:
        prodDesc = "No Description"
    return prodDesc


"""
    Function to scrap product ratings count from the flipcart page
    Requires one argument (i.e, source code of the page)
    Returns product ratings count as list of dictionary
"""
def get_product_ratings(page):
    reviewsAndRatings = page.findAll("div", {"class": "row _3AjFsn _2c2kV-"})
    reviewRatings = []

    # Overall rating count of the product
    try:
        overallRating = reviewsAndRatings[0].find_all("div", {"class": "_2d4LTz"})[0].text
    except:
        overallRating = '0'

    # Total no of people rated the product
    try:
        ratingCount = reviewsAndRatings[0].find_all("div", {"class": "row _2afbiS"})[0].text
    except:
        ratingCount = '0'

    # Total no of reviews for the product
    try:
        reviewCount = reviewsAndRatings[0].find_all("div", {"class": "row _2afbiS"})[1].text
    except:
        reviewCount = '0'

    ratings = dict(overallRating=overallRating, ratingCount=ratingCount, reviewCount=reviewCount)

    # Rating chart (5,4,3,2,1 stars individually)
    try:
        startsCountAll = reviewsAndRatings[0].find_all("div", {"class": "_1uJVNT"})
        startsCount = {}
        n = len(startsCountAll)
        for star in range(n):
            startsCount[str(n - star)] = startsCountAll[star].text
    except:
        startsCount = {'1': '0', '2': '0', '3': '0', '4': '0', '5': '0'}

    # Product feature ratings
    try:
        featureName = reviewsAndRatings[0].find_all("div", {"class": "_3npa3F"})
        featureRating = reviewsAndRatings[0].find_all("text", {"class": "_2Ix0io"})
        featureNameRating = {}
        for feature in range(len(featureName)):
            name = featureName[feature].text
            rate = featureRating[feature].text
            featureNameRating[name] = rate
    except:
        featureNameRating = {'No features': '0'}

    reviewRatings.append(ratings)
    reviewRatings.append(startsCount)
    reviewRatings.append(featureNameRating)

    return reviewRatings


"""
    Function to scrap customer comments for the product from the flipcart page
    Requires one argument (i.e, source code of the page)
    Returns comments as list of dictionary
"""
def get_product_comments(page):

    commentsPageLink = "https://www.flipkart.com" + page.findAll("div", {"class": "col JOpGWq"})[0].findAll("a")[-1]['href']
    commentsPage = requests.get(commentsPageLink)  # Request webpage from internet
    commentsPage = BeautifulSoup(commentsPage.text, "html.parser")  # Parse web page as html
    links = commentsPage.findAll("nav", {"class": "yFHi8N"})[0].findAll("a")
    commentLinks = []
    for a in links:
        link = "https://www.flipkart.com" + a['href']
        commentLinks.append(link)
    commentLinks = commentLinks[:10]


    reviews = []
    for link in commentLinks:
        page = requests.get(link)  # Request webpage from internet
        page = BeautifulSoup(page.text, "html.parser")  # Parse web page as html

        commentBoxes = page.findAll("div", {"class": "col _2wzgFH K0kLPL"})  # Select all comments

        # This for loop will iterate through each comments and retrieve all the information from it.
        # Information line Comment name, rating, heading, review
        for cBox in commentBoxes:
            try:
                name = cBox.find_all("p", {"class": "_2sc7ZR _2V5EHH"})[0].text  # Name of the customer
            except:
                name = 'No Name'

            try:
                rating = cBox.find_all("div", {"class": "_3LWZlK _1BLPMq"})[0].text  # Rating given by the customer
            except:
                rating = 'No Rating'

            try:
                commentHead = cBox.find_all("p", {"class": "_2-N8zT"})[0].text  # Review heading given by the customer
            except:
                commentHead = 'No Comment Heading'

            try:
                customerComment = cBox.find_all("div", {"class": "t-ZTKy"})[0].div.text  # Review by customer
                customerComment = customerComment.replace("READ MORE", "")
            except:
                customerComment = 'No Customer Comment'

            reviewDictionary = dict(Name=name, Rating=rating, CommentHead=commentHead,
                                    Comment=customerComment)  # Store retrieved information as a dictionary
            reviews.append(reviewDictionary)

    return reviews


"""
    Function to scrap details about the product from the flipcart page
    Requires two arguments (i.e, product page link and source code of the page)
    Returns list of product details.
"""
def get_details(link, page):
    scrappedContent = []  # List to store details of the product

    productLink = link
    productName = get_product_name(page)  # Scrap product name from the page
    productImage = get_product_image(page)  # Scrap product image from the page
    productHighlights = get_product_highlights(page)  # Scrap product highlights from the page
    productDescription = get_product_description(page)  # Scrap product description from the page
    productRatings = get_product_ratings(page)  # Scrap product ratings from the page
    productReviews = get_product_comments(page)  # Scrap product comments from the page

    # Append all the scrapped details of the product into list
    scrappedContent.append(dict(productName=productName))
    scrappedContent.append(dict(productLink=productLink))
    scrappedContent.append(dict(productImage=productImage))
    scrappedContent.append(dict(prductHighlights=productHighlights))
    scrappedContent.append(dict(productDescription=productDescription))
    scrappedContent.append(dict(productRatings=productRatings))
    scrappedContent.append(dict(productReviews=productReviews))

    result = {'product': scrappedContent}  # Create dictionary with product name as key and details as values
    return result   # Result returned to app.py