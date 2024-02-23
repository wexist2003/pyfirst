import json
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

MAX_RETRIES = 10

unique_authors = set()
start_url = "https://quotes.toscrape.com"
with open("authors.json", "w", encoding="utf-8") as file:
    json.dump([], file, ensure_ascii=False, indent=4)


def save_author_info(author_info):
    with open("authors.json", "r", encoding="utf-8") as file:
        authors_data = json.load(file)

    if author_info["fullname"] not in unique_authors:
        authors_data.append(author_info)
        unique_authors.add(author_info["fullname"])

    with open("authors.json", "w", encoding="utf-8") as file:
        json.dump(authors_data, file, ensure_ascii=False, indent=4)


def get_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, "lxml")

    fullname = soup.find("h3", class_="author-title").text
    born_info = soup.find("span", class_="author-born-date").text
    born_location = soup.find("span", class_="author-born-location").text
    description = soup.find("div", class_="author-description").text

    author_info = {
        "fullname": fullname,
        "born_date": born_info,
        "born_location": born_location,
        "description": description.strip()
    }

    return author_info


def save_data(next):
    url = next
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    tags = soup.find_all("div", class_="tags")
    link_authors = [
        f'{start_url}{tag.select_one("span a")["href"]}'
        for tag in soup.find_all("div", class_="quote")
    ]

    data = []

    for i in range(0, len(quotes)):
        quote_text = (
            quotes[i].text.replace("\u201c", '"').replace("\u201d", '"').strip('"')
        )
        author_name = authors[i].text.encode("latin1").decode("unicode_escape")
        author_url = link_authors[i]
        print(author_url)
        tags_for_quote = [tag.text for tag in tags[i].find_all("a", class_="tag")]

        quote_data = {
            "tags": tags_for_quote,
            "author": author_name,
            "quote": quote_text,
        }

        author_info = get_author_info(author_url)
        save_author_info(author_info)

        data.append(quote_data)

    next = soup.select_one("li.next a")
    return next, data


if __name__ == "__main__":
    url = start_url
    next_url = url
    all_quotes_data = []
    while next_url:
        next_url, quotes_data = save_data(next_url)
        all_quotes_data.extend(quotes_data)
        if next_url:
            href = next_url["href"]
            page_number = href.split("/")[-2]
            next_url = f"{url}{href}"
            print(f"Go to NEXT {next_url}")
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(all_quotes_data, file, ensure_ascii=False, indent=4)
    print("Done!")
