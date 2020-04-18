import requests
import os

url_list = []


def clear():
    return os.system('clear')
    # if system os is 'windows' -> return os.system('cls')


while(True):
    print("Welcome to IsItDown.py!")
    print("Please write a URL or URLs you wnat to check. (separated by comma)")

    value = input('please input url: \n')
    url_list = value.split(',')
    for url in url_list:
        if url.find(".com") == -1:
            print(f"{url} is not a valid URL")
            break
        url = url.replace("http://", "")
        url = url.strip('cmowz. ')
        url = 'http://' + url + '.com'
        url = url.lower()
        try:
            r = requests.get(url)
            if r.status_code == requests.codes.ok:
                print(f"{url} is up")
            else:
                print(f"{url} is down")
        except:
            print(f"{url} is down")

    q = input("Do you want to start over? y/n ")
    if q == 'y':
        clear()
        continue
    elif q == 'n':
        print("Ok. Bye")
        break
    else:
        print("That's not a valid answer")
        q = input("Do you want to start over? y/n ")
        if q == 'y':
            clear()
            continue
        elif q == 'n':
            print("Ok. Bye")
            break
