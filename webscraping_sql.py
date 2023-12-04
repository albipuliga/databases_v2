import os
import django
import pandas as pd
import requests

# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "databases_v2.settings")
django.setup()

from databases_v2_app.models import Author, Book


def get_isbn_list(file_path: str) -> list[str]:
    """Read the CSV file (the ISBN column specifically) and return a list of ISBNs that will then be used for API calls to Open Library."""
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Extract the ISBN column into a list
    isbn_list = df["isbn"].tolist()

    return isbn_list


def get_book_details_by_isbn(isbn_list: list[str]) -> None:
    """
    For each ISBN in the list, make an API call to Open Library to retrieve the book details:
        - title
        - author
        - publisher
        - number of pages
    Then, create or update the book in your database."""
    for isbn in isbn_list:
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        try:
            # Get request to Open Library API
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the book data from the response
                book_data = response.json().get(f"ISBN:{isbn}", {})

                title = book_data.get("title")
                authors = book_data.get("authors", [])
                publishers = book_data.get("publishers", [])
                number_of_pages = book_data.get("number_of_pages")

                if title and authors:
                    # Create or update the author in your database
                    author_name, key = (
                        authors[0].get("name"),
                        (authors[0].get("url")).split("/")[-2] or "",
                    )  # Assuming the first author
                    author, created = Author.objects.get_or_create(
                        name=author_name, key=key
                    )
                    # Create or update the book in your database
                    book, created = Book.objects.update_or_create(
                        title=title,
                        defaults={
                            "author": author,
                            "isbn": isbn,
                            "publishers": ", ".join(
                                p.get("name", "") for p in publishers
                            ),
                            "number_of_pages": number_of_pages or 0,
                        },
                    )
                    print(f'{"Created" if created else "Updated"}: {book.title}')
                else:
                    print(f"No detailed information found for ISBN {isbn}")
            else:
                print(
                    f"Failed to retrieve data for ISBN {isbn}. Status code: {response.status_code}"
                )
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the API call for ISBN {isbn}: {e}")


isbn_list = get_isbn_list("books.csv")
get_book_details_by_isbn(isbn_list)
