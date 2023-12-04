import streamlit as st
import django
import os

# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "databases_v2.settings")
django.setup()

from databases_v2_app.models import Book, Author

# Streamlit app
st.markdown("# Library Database :books:")
st.markdown("### Search for books, authors, and publishers in our database.")


# Function to search books
def search_books(field, query):
    # If no title is specified, return all books; else, return books by title
    if field == "Title":
        return (
            Book.objects.filter(title__icontains=query) if query else Book.objects.all()
        )
    # If no author is specified, return all authors; else, return books by author
    elif field == "Author":
        if query:
            authors = Author.objects.filter(name__icontains=query)
            return Book.objects.filter(author__in=authors)
        else:
            return Author.objects.all()
    elif field == "Publisher":
        return (
            Book.objects.filter(publishers__icontains=query)
            if query
            else Book.objects.all()
        )
    elif field == "ISBN":
        return Book.objects.filter(isbn__icontains=query)


# User input
search_option = st.selectbox(
    "Select search type:", ["Title", "Author", "Publisher", "ISBN"]
)
search_query = st.text_input("Enter search query:")

# Pagination
PAGE_SIZE = 10
page_number = st.number_input("Page number", min_value=1, value=1)
start_index = (page_number - 1) * PAGE_SIZE
end_index = start_index + PAGE_SIZE

# Button to perform search
if st.button("Search"):
    # Perform search
    if search_option == "Author" and search_query == "":
        results = Author.objects.all()
        if results.exists():
            for author in results:
                st.markdown(f"<h3>Name: {author.name}</h3>", unsafe_allow_html=True)
                st.markdown(f"<h3>Key: {author.key}</h3>", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.markdown(f"**No results found for** *'{search_query}'*")

    elif search_option == "Publisher" and search_query == "":
        results = Book.objects.filter(publishers__isnull=False).values_list(
            "publishers", flat=True
        )
        if results.exists():
            # Get unique publishers using a set
            unique_publishers = set(results)
            for publisher in unique_publishers:
                st.markdown(f"<h3>{publisher}</h3>", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.markdown(f"**No results found for** *'{search_query}'*")

    else:
        results = search_books(search_option, search_query)[start_index:end_index]
        # Display results
        if results.exists():
            for book in results:
                st.markdown(f"<h3>Title: {book.title}</h3>", unsafe_allow_html=True)
                st.markdown(
                    f"<h3>Author: {book.author.name}</h3>", unsafe_allow_html=True
                )
                st.markdown(f"**Publisher:** {book.publishers}")
                st.markdown(f"**ISBN:** {book.isbn}")
                st.markdown(f"**Number of Pages:** {book.number_of_pages}")
                st.markdown("---")
        else:
            st.markdown(f"**No results found for** *'{search_query}'*")
