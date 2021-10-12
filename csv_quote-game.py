from bs4 import BeautifulSoup
import requests
from time import sleep
from random import choice
from csv import DictReader

base_url = "https://quotes.toscrape.com/"


def read_quote(filename):
    with open(filename, 'r') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(quotes):

    quote = choice(quotes)
    remaining_guesses = 4
    print("here is a quote : ")
    print(quote["text"])
    print(quote["author"])
    guess = ""

    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(
            f"who said this quote? Guesses remaining: {remaining_guesses} ")
        if guess.lower() == quote["author"].lower():
            print('you got it right')
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(f"{base_url}{quote['bio_link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_place = soup.find(class_="author-born-location").get_text()
            print(
                f"here is a hint : The author was born on {birth_date}  {birth_place}")
        elif remaining_guesses == 2:
            print(
                f"here is a hint : the authors first name is : {quote['author'][0]}")
        elif remaining_guesses == 1:
            last_initial = quote["author"].split(" ")[1][0]
            print(
                f"here is a hint: The authors last name starts with: {last_initial}")
        else:
            print(
                f"Sorry ran out of guesses , the answer is {quote['author']}")

    again = ""
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("want to play again (y/n)?")
        if again.lower() in ('yes', 'y'):
            return start_game(quotes)
            print("okay you play again ")
        else:
            print("ok goodbye")


quotes = read_quote("quotes.csv")
start_game(quotes)
