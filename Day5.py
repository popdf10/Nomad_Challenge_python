import os
import requests
from bs4 import BeautifulSoup

country_list = []

os.system("clear")
url = "https://www.iban.com/currency-codes"


def extract_country(table):
    lists = []
    td = table.find_all("td")
    for element in td:
        if element.get_text() == '':
            return
        lists.append(element.get_text())
    return {
        "country": lists[0].lower().capitalize(),
        "currency": lists[1],
        "code": lists[2],
        "num": lists[3]
    }


def extract_table():
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    table_list = soup.find("table").find("tbody").find_all("tr")
    for column in table_list:
        country_dict = extract_country(column)
        if country_dict == None:
            continue
        country_list.append(country_dict)


def main():
    extract_table()
    print("Hello! Please choose select a country by number:")
    for index, country in enumerate(country_list):
        print(f"# {index} {country.get('country')}")
    restart()


def restart():
    try:
        chose_num = int(input('#: '))
        chose = country_list[chose_num]
        print(f"You chose {chose.get('country')}")
        print(f"The currency code is {chose.get('code')}")
    except ValueError:
        print("That wasn’t a number.")
        restart()
    except IndexError:
        print("choose a number from the list")
        restart()


main()
