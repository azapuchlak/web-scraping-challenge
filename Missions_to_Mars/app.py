# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Use 'Find one' to find a record of data from the mongodb
    mars_record = mongo.db.mars_record.find_one()
    # Return
    return render_template("index.html", mars=mars_record)


@app.route("/scrape")
def scrape():
  
    mars_record = mongo.db.mars_record
    mars_data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_record.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)