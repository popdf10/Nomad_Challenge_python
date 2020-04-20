import os
import csv
import requests
from bs4 import BeautifulSoup

# os.system("clear")
os.system("cls")
alba_url = "http://www.alba.co.kr"

company_list = []
link_list = []

brand_list = []
detail_info = []

result = requests.get(alba_url).text
soup = BeautifulSoup(result, "html.parser")
finded_ul = soup.find("div", {"id": "MainSuperBrand"})

links_info = finded_ul.find("ul", {"class": "goodsBox"}).find_all("li")
links_info = links_info[:-3]
for link in links_info:
    href = link.find("a")["href"]
    link_list.append(href)

companys_info = finded_ul.find_all("a", {"class": "goodsBox-info"})
for companys in companys_info:
    company = companys.find("span", {"class": "company"}).get_text()
    company_list.append(company)

for i in range(len(company_list)):
    brand_list.append({'company': company_list[i], 'link': link_list[i]})


def extract_detail_company_info(url):
    info = []
    r = requests.get(url).text
    soup = BeautifulSoup(r, "html.parser")
    tables = soup.find("div", {"id": "NormalInfo"}).find(
        "tbody").find_all("tr", {"class": ""})

    for table in tables:
        if table.find("td").get_text() == "해당 조건/분류에 일치하는 채용정보가 없습니다.":
            return "해당 조건/분류에 일치하는 채용정보가 없습니다."
        place = table.find("td", {"class": "local first"}
                           ).get_text().replace("\xa0", " ")
        title = table.find("td", {"class": "title"}).find(
            "span", {"class": "company"}).get_text()
        time = table.find("td", {"class": "data"}).get_text()
        pay = table.find("td", {"class": "pay"}).find(
            "span", {"class": "payIcon"}).get_text() + table.find("td", {"class": "pay"}).find(
            "span", {"class": "number"}).get_text()
        date = table.find("td", {"class": "regDate"}).get_text()
        #date = table.find("td", {"class": "regDate"}).find("strong").get_text()

        info.append({'place': place, 'title': title,
                     'time': time, 'pay': pay, 'date': date})

    return info


def make_csv(detail):
    try:
        comp_title = detail.get('company')
        print(comp_title)
        if detail.get('link') == 'http://www.alba.co.kr/job/brand/elandfashion/job/brand/?page=1&pagesize=50':
            return
        elif detail.get('link') == 'http://www.alba.co.kr/job/brand/elandintro/job/brand/?page=1&pagesize=50':
            return
        else:
            temp_url = detail.get('link') + "job/brand/?page=1&pagesize=50"
            print(temp_url)
            detail_info = extract_detail_company_info(temp_url)
    except AttributeError:
        return

    file = open(f"{comp_title}.csv", mode="w", encoding='utf-8', newline='')
    writer = csv.writer(file)

    if detail_info == "해당 조건/분류에 일치하는 채용정보가 없습니다.":
        writer.writerow([detail_info])
        return

    writer.writerow(['place', 'title', 'time', 'pay', 'date'])

    for info in detail_info:
        writer.writerow(list(info.values()))


for comp_detail in brand_list:
    make_csv(comp_detail)
