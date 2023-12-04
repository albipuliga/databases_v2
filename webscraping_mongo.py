import re
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# algorithm
# ---------
# map classes or properties with keywords for getting data

# enter main website
#   get the data available there and store it (book a)
# go to individual book (book a)
#   get the data available there and store it (book a)
# go back with driver.back()
#   get the data available there and store it (book b)


def scrape_paragraph(url):
    # Send an HTTP request to the website and get the content
    response = requests.get(url)
    code = response.status_code

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        return f"Failed to retrieve the webpage. Status code: {response.status_code}"

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the paragraph (you might need to inspect the HTML structure of the website)
    paragraph = soup.find("span", class_="Formatted")

    # Check if a paragraph was found
    if paragraph:
        # Extract the text content of the paragraph
        paragraph_text = paragraph.get_text()
        return paragraph_text
    else:
        return "No paragraph found on the website."


def scrape_books(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    # regular expression for any 4 digit number
    patternForYears = r"\b\d{4}\b"

    for book_elem in soup.find_all("tr", itemtype="http://schema.org/Book"):
        # Extracting book details
        # title
        title_elem = book_elem.find("a", class_="bookTitle")
        # author
        author_elem = book_elem.find("a", class_="authorName")
        # average rating
        rating_elem = book_elem.find("span", class_="minirating")
        # year published
        published_elem = book_elem.find("span", class_="greyText smallText uitext")
        # description of book
        description_elem = scrape_paragraph(
            # URL including goodreads.com/ before
            "https://goodreads.com"
            + str(book_elem.find("a", class_="bookTitle").get("href"))
        )

        # Extracting additional details
        avg_rating = rating_elem.text.strip().split()[0] if rating_elem else "N/A"
        ratings_count = rating_elem.text.strip().split()[4] if rating_elem else "N/A"

        thereIsYear = re.search(patternForYears, published_elem.text)
        if thereIsYear:
            published_year = thereIsYear.group()
        else:
            published_year = "N/A"

        description = description_elem if description_elem else "N/A"

        book_info = {
            "title": title_elem.text.strip() if title_elem else "N/A",
            "author": author_elem.text.strip() if author_elem else "N/A",
            "average_rating": avg_rating if avg_rating else "N/A",
            "ratings_count": ratings_count if avg_rating else "N/A",
            "published_year": published_year,
            "description": description,
        }

        books.append(book_info)

    return books


def connect_to_mongo(dicdata):
    # Stablishes the connections makes or updates the database/connection
    client = MongoClient("mongodb://localhost:27017")
    db = client["library_database"]
    collection = db["library_database_collection"]
    # inserts the data into mongo
    collection.insert_many(dicdata)
    client.close()


def main():
    # goodreads for now
    mainURL = (
        "https://www.goodreads.com/search?page=99&q=books&qid=I5rZPmqzTS&tab=books"
    )
    # gets the dictionaries from the function
    scraped_books = scrape_books(mainURL)

    # if dictionaries are returned it connects to mongo and uploads the data and prints it did so, otherwise it prints that it didn't
    if scraped_books:
        connect_to_mongo(scraped_books)
        print("Data successfully inserted into MongoDB.")
    else:
        print("No data to insert into MongoDB.")


main()
