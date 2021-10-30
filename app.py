from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   # uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. 
   # We will also assign that path to themars variable for use later.
   mars = mongo.db.mars.find_one()

   # tells Flask to return an HTML template using an index.html file. We'll create this file after we build the Flask routes.
   # mars = mars tells python to use mars collection in  MongoDB
   return render_template("index.html", mars=mars)


@app.route("/scrape")
# This route will be the "button" of the web application, the one that will scrape updated data when we tell it to from the homepage of our web app. It'll be tied to a button that will run the code when it's clicked.
# defines the route that Flask will be using. This route, “/scrape”, will run the function that we create just beneath it.
def scrape():
   # new variable that points to our Mongo database:
   mars = mongo.db.mars
   # new variable to hold the newly scraped data: mars_data = scraping.scrape_all(). 
   # In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.
   mars_data = scraping.scrape_all()
   # update the database
   # 1) add an empty JSON object with {} in place of the query_parameter
   # 2) data we have stored in mars_data
   # 3) upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if we haven't already created a document for it).
   mars.update({}, mars_data, upsert=True)
   # navigate our page back to / where we can see the updated content.
   return redirect('/', code=302)


if __name__ == "__main__":
   app.run()