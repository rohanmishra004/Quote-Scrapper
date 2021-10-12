from bs4 import BeautifulSoup
import requests
from time import sleep
from random import choice
from csv import DictWriter

base_url = "https://quotes.toscrape.com/"


def scrape_quotes():
    url = "/page/1"
    all_quotes = []
    while url:
        res = requests.get(f"{base_url}{url}")
        # print(f"Now Scrapping {base_url}{url}")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")
        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio_link": quote.find("a")["href"]
            })

        nxt_button = soup.find(class_="next")
        url = nxt_button.find("a")["href"] if nxt_button else None
        # sleep(2)
    return all_quotes


def write_quotes(quotes):
    # write quotes to csv file
    with open('quotes.csv', 'w') as file:
        headers = ["text", "author", "bio_link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)


quotes = scrape_quotes()
write_quotes(quotes)
