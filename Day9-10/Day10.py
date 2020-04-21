import requests
import json
from flask import Flask, render_template, request

db = {}
popular_list = []
new_list = []

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new_url = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular_url = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api

popular = requests.get(popular_url).text
parsed_popular = json.loads(popular)['hits']
db['popular'] = parsed_popular

new = requests.get(new_url).text
parsed_new = json.loads(new)['hits']
db['new'] = parsed_new


def make_detail_url(id):
    return f"{base_url}/items/{id}"


def extract_list(db):
    for popular in db.get('popular'):
        title = popular.get('title')
        url = popular.get('url')
        author = popular.get('author')
        points = popular.get('points')
        num_comments = popular.get('num_comments')
        popular_list.append({'title': title, 'url': url, 'author': author,
                             'points': points, 'num_comments': num_comments})

    for new in db.get('new'):
        title = new.get('title')
        url = new.get('url')
        author = new.get('author')
        points = new.get('points')
        num_comments = new.get('num_comments')
        new_list.append({'title': title, 'url': url, 'author': author,
                         'points': points, 'num_comments': num_comments})


extract_list(db)

app = Flask("DayNine")


@app.route("/")
def home():
    order_by = request.args.get('order_by')
    if order_by == 'new':
        return render_template("new.html", new_list=new_list)
    elif order_by == 'popular':
        return render_template("index.html", popular_list=popular_list)
    return render_template("index.html", popular_list=popular_list)


@app.route("/detail")
def detail():
    return render_template("detail.html")


app.run(host="127.0.0.1")
