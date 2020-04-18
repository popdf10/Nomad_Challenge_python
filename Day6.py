import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

country_list = []

os.system("clear")
country_url = "https://www.iban.com/currency-codes"


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
    result = requests.get(country_url)
    soup = BeautifulSoup(result.text, "html.parser")
    table_list = soup.find("table").find("tbody").find_all("tr")
    for column in table_list:
        country_dict = extract_country(column)
        if country_dict == None:
            continue
        country_list.append(country_dict)


def extract_currency(country_code1, country_code2, money):
    currency_url = f"https://transferwise.com/gb/currency-converter/{country_code1}-to-{country_code2}-rate"
    result = requests.get(currency_url, {"amount": money})
    soup = BeautifulSoup(result.text, "html.parser")
    currency_result = soup.find("input", {"class": "js-TargetAmount"})["value"]
    return currency_result


def main():
    extract_table()
    print("Welcom to Currencyconvert PRO 2000")
    for index, country in enumerate(country_list):
        print(f"# {index} {country.get('country')}")
    restart()


def restart():
    try:
        print("\nWhere are you from? Choose a country by number.\n")
        chose_num = int(input('#: '))
        country_num1 = country_list[chose_num]
        print(f"{country_num1.get('country')}\n")

        print("Now choose another country.\n")
        chose_num = int(input('#: '))
        country_num2 = country_list[chose_num]
        print(f"{country_num2.get('country')}\n")

        re_restart(country_num1, country_num2)

    except ValueError:
        print("That wasn’t a number.\n")
        restart()

    except IndexError:
        print("choose a number from the list\n")
        restart()


def re_restart(country_num1, country_num2):
    try:
        print(
            f"How many {country_num1.get('code')} do you want to convert to {country_num2.get('code')}?")
        money = int(input())
        converted_currency = extract_currency(country_num1.get('code'),
                                              country_num2.get('code'), money)
        converted_currency = format_currency(
            converted_currency, country_num2.get('code'), locale="ko_KR")
        formatted_currency = format_currency(
            money, country_num1.get('code'), locale="ko_KR")
        print(
            f"{country_num1.get('code')} {formatted_currency} is {converted_currency}")
    except ValueError:
        print("That wasn’t a number.\n")
        re_restart(country_num1, country_num2)


main()
