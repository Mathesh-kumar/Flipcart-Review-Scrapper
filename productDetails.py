"""
This is used to product details from the flipcart site
Used to retrieve details like reviewer name, rating, comment and so on
"""

# from bs4 import BeautifulSoup  # Makes easy to scrap contents from web page

def get_details(uniqueProductPage):

    pageReviews = []
    commentBoxes = uniqueProductPage.findAll("div", {"class": "col _2wzgFH"})  # Select all comments

    reviewsAndRatings = uniqueProductPage.findAll("div", {"class": "row _3AjFsn _2c2kV-"})
    reviewRatings = []
    try:
        overallRating = reviewsAndRatings[0].find_all("div", {"class": "_2d4LTz"})[0].text
    except:
        overallRating = '0'

    try:
        ratingCount = reviewsAndRatings[0].find_all("div", {"class": "row _2afbiS"})[0].text
    except:
        ratingCount = '0'

    try:
        reviewCount = reviewsAndRatings[0].find_all("div", {"class": "row _2afbiS"})[1].text
    except:
        reviewCount = '0'

    ratings = dict(overallRating=overallRating, ratingCount=ratingCount,reviewCount=reviewCount)

    try:
        startsCountAll = reviewsAndRatings[0].find_all("div", {"class": "_1uJVNT"})
        startsCount = {}
        n = len(startsCountAll)
        for star in range(n):
            startsCount[str(n-star)] = startsCountAll[star].text
    except:
        startsCount = '0'

    try:
        featureName = reviewsAndRatings[0].find_all("div", {"class": "_3npa3F"})
        featureRating = reviewsAndRatings[0].find_all("text", {"class": "_2Ix0io"})
        featureNameRating = {}
        for feature in range(len(featureName)):
            name = featureName[feature].text
            rate = featureRating[feature].text
            featureNameRating[name] = rate
    except:
        featureNameRating = '0'

    reviewRatings.append(ratings)
    reviewRatings.append(startsCount)
    reviewRatings.append(featureNameRating)


    try:
        prodName = uniqueProductPage.find_all("h1", {"class": "yhB1nd"})[0].text  # Name of the product
    except:
        prodName = "No Name"

    pageReviews.append(dict(prodName=prodName))
    pageReviews.append(dict(reviewRatings=reviewRatings))
    prodName = prodName[:16]

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
        pageReviews.append(reviewDictionary)

    result = {prodName: pageReviews}
    return result