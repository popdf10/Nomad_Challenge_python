import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import operator
import time

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]


def scrape_reddit(list):
    card_list = []
    for subreddit in list:
        url = f"https://www.reddit.com/r/{subreddit}/top/?t=month"
        r = requests.get(url, headers=headers).text
        soup = BeautifulSoup(r, "html.parser")
        cards = soup.find("div", {"class": "rpBJOHq2PR60pnwJlUyP0"}).find_all(
            "div", {"class": "_1oQyIsiPHYt6nx7VOmd1sz"})

        for card in cards:
            upvote = card.find(
                "div", {"class": "_1rZYMD_4xY3gRcSS3p8ODO"}).text
            if upvote == "•":
                continue
            else:
                try:
                    upvote = int(upvote)
                except ValueError:
                    continue
            title = card.find("h3").text
            url = card.find("a", {"class": "SQnoC3ObvgnGjWt90zD9Z"})
            if url != None:
                url = url["href"]
            card_list.append({'upvote': upvote, 'title': title,
                              'url': url, 'subreddit': subreddit})
    card_list.sort(key=operator.itemgetter('upvote'), reverse=True)

    return card_list


app = Flask("DayEleven")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/read")
def read():
    extract_reddits = []
    start_time = time.time()
    for reddit in subreddits:
        if request.args.get(reddit):
            extract_reddits.append(reddit)

    reddit_list = scrape_reddit(extract_reddits)
    elapsed_time = time.time() - start_time

    print(f"{elapsed_time} milliseconds")
    return render_template("read.html", reddit_list=reddit_list, reddit_item=extract_reddits)


app.run(host="127.0.0.1")
