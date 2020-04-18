import requests
from bs4 import BeautifulSoup
import json

# gbp-to-usd-rate?amount = 50

code1 = "GBP"
code2 = "USD"

currency_url = "https://transferwise.com/gb/currency-converter/gbp-to-usd-rate"
currency_url = f"https://transferwise.com/gb/currency-converter/{code1}-to-{code2}-rate"

temp_dict = {'amount': '50'}

result = requests.get(currency_url, temp_dict)
soup = BeautifulSoup(result.text, "html.parser")
currency_result = soup.find("input", {"class": "js-TargetAmount"})["value"]
print(currency_result)
