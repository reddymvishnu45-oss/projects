from flask import Flask, request, redirect, render_template
from pymongo import MongoClient
import string
import random

app = Flask(__name__)

# MongoDB Connection (GLOBAL)
client = MongoClient("mongodb://localhost:27017/")
db = client["url_shortener"]
collection = db["urls"]


# Generate random short code
def generate_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


# Generate unique code (MongoDB version)
def generate_unique_code():
    while True:
        code = generate_code()
        if not collection.find_one({"short": code}):
            return code


@app.route("/", methods=['GET', 'POST'])
def home():
    short_url = None

    if request.method == 'POST':
        long_url = request.form['url']

        # Fix missing http
        if not long_url.startswith("http"):
            long_url = "http://" + long_url

        code = generate_unique_code()

        # Insert into MongoDB
        collection.insert_one({
            "short": code,
            "long": long_url
        })

        short_url = request.host_url + code

    return render_template('index.html', short_url=short_url)


@app.route("/<code>")
def redirect_url(code):
    result = collection.find_one({"short": code})

    if result:
        return redirect(result["long"])
    else:
        return "<h3>URL not found</h3>", 404


# View all URLs
@app.route("/list")
def list_urls():
    data = list(collection.find({}, {"_id": 0}))
    return str(data)


if __name__ == "__main__":
    app.run(debug=True)