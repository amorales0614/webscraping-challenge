from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri='mongodb://localhost:27017/mars_app')

@app.route("/")
def home():

    home_data = mongo.db.mars_dict.find_one()
    print (home_data)
    return render_template("index.html", mars=home_data)

@app.route("/scrape")
def scrape():
  
    home_data = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()
    print (mars_data)
    home_data.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)