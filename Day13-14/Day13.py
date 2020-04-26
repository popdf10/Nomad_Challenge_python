import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, send_file
import csv

db = {}


def extract_job(url):
    temp_list = []
    # extracting StackOverflow jobs
    result = requests.get(url[0]).text
    soup = BeautifulSoup(result, "html.parser")
    cards = soup.find("div", {"class": "listResults"}).find_all("div", {"class": "grid--cell fl1"})

    for card in cards:
        card_a = card.find("h2", {"class": "mb4 fc-black-800 fs-body3"})
        title = card.find("a")["title"]
        link = "https://stackoverflow.com" + card.find("a")["href"]
        company = card.find("h3", {"class": "fc-black-700 fs-body1 mb4"}).find("span").text.strip()

        temp_list.append({'title': title, 'link': link, 'company': company})

    # extracting WeWork jobs 
    result = requests.get(url[1]).text
    soup = BeautifulSoup(result, "html.parser")
    cards = soup.find("section", {"class": "jobs"}).find("ul").find_all("li")

    for card in cards:
        link = "https://weworkremotely.com" + card.find("a")["href"]
        title = card.find("span", {"class": "title"})
        if title != None:
            title = title.text
        company = card.find("span", {"class": "company"})
        if company != None:
            company = company.text
        
        temp_list.append({'title': title, 'link': link, 'company': company})


    # extracting RemoteOk jobs
    result = requests.get(url[2]).text
    soup =BeautifulSoup(result, "html.parser")
    cards = soup.find("table", {"id": "jobsboard"}).find_all("tr", {"class": "job"})
    for card in cards:
        company = card.find("td", {"class": "company position company_and_position"}).find("a", {"itemprop": "hiringOrganization"}).find("h3").text
        title = card.find("td", {"class": "company position company_and_position"}).find("h2", {"itemprop": "title"}).text
        link = "https://remoteok.io" + card["data-href"]

        temp_list.append({'title': title, 'link': link, 'company': company})
    
    return temp_list


def save_to_file(jobs, name):
    file = open(f"csv/{name}.csv", mode='w', encoding='utf-8', newline='')
    writer = csv.writer(file)
    writer.writerow(["title", "link", "company"])
    for job in jobs:
        writer.writerow(job.values())
    print("All Jobs save safety!")
    return

app = Flask("Final Homework")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search")
def search():
    name = request.args.get('term').lower()
    url_list = []
    url_list.append(f"https://stackoverflow.com/jobs?r=true&q={name}")
    url_list.append(f"https://weworkremotely.com/remote-jobs/search?term={name}")
    url_list.append(f"https://remoteok.io/remote-dev+{name}-jobs")

    if db.get(name):
        job_list = db.get(name)
    else:
        job_list = extract_job(url_list)
        db[name] = job_list
    
    
    return render_template("search.html", job_list=job_list, length=len(job_list), name=name)

@app.route("/export")
def export():
    try:
        word = request.args.get('term').lower()
        if not word:
            raise Exception()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
    except:
        redirect("/")
    save_to_file(jobs, word)
    
    return send_file(f"csv/{word}.csv", as_attachment=True)

app.run(host="127.0.0.1")